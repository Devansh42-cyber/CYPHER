from flask import Flask, render_template, request, jsonify
import os
import joblib
from src.feature_extraction import extract_features


# -----------------------
# Configuration (from environment variables)
# -----------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_ENV = os.environ.get("APP_ENV", "development")
APP_VERSION = os.environ.get("APP_VERSION", "dev")
PORT = int(os.environ.get("PORT", "5000"))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
MODEL_PATH = os.environ.get(
    "MODEL_PATH", os.path.join(BASE_DIR, "model", "phishing_model.pkl")
)


# -----------------------
# Flask Setup
# -----------------------

app = Flask(__name__)

# Static files are referenced with ?v=<version>, so browsers and CloudFront can cache them for a year;
# a new deploy changes the version and therefore the URL.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000


@app.context_processor
def inject_version():
    # Available in every template: used for the footer and for cache-busting static assets
    return {"app_version": APP_VERSION, "app_env": APP_ENV}


# -----------------------
# Load ML Model
# -----------------------

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("[INFO] Phishing model loaded successfully.")
else:
    model = None
    print("[WARNING] Model file not found. Train model first!")


# -----------------------
# Dashboard Stats
# -----------------------

dashboard_stats = {
    "total": 0,
    "phishing": 0,
    "legitimate": 0,
}


# -----------------------
# Routes
# -----------------------

@app.route('/')
def loading():
    return render_template('Loading.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/contact')
def contact():
    return render_template('Contact.html')


# -----------------------
# Health check (used by Docker, the deploy script and monitoring)
# -----------------------

@app.route('/health')
def health():
    status = "ok" if model is not None else "degraded"
    code = 200 if model is not None else 503
    return jsonify({
        "status": status,
        "model_loaded": model is not None,
        "version": APP_VERSION,
        "env": APP_ENV,
    }), code


# -----------------------
# API: URL Prediction
# -----------------------

@app.route('/check_url_api', methods=['POST'])
def check_url_api():

    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL not provided"}), 400

    try:
        features = extract_features(url)
        prediction = model.predict([features])[0]

        result = "Phishing" if prediction == 1 else "Legitimate"

        # Update dashboard stats
        dashboard_stats["total"] += 1

        if result == "Phishing":
            dashboard_stats["phishing"] += 1
        else:
            dashboard_stats["legitimate"] += 1

        return jsonify({
            "url": url,
            "prediction": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_dashboard_stats")
def get_dashboard_stats():
    return jsonify(dashboard_stats)


# -----------------------
# Run Application (local development only; Docker uses gunicorn)
# -----------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
