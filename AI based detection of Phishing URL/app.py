from flask import Flask, render_template, request, jsonify
import os
import joblib
from src.feature_extraction import extract_features


# -----------------------
# Flask Setup
# -----------------------

app = Flask(__name__)


# -----------------------
# Load ML Model
# -----------------------

MODEL_PATH = os.path.join("model", "phishing_model.pkl")

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
# API: URL Prediction
# -----------------------

@app.route('/check_url_api', methods=['POST'])
def check_url_api():

    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
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
# Run Application
# -----------------------

if __name__ == '__main__':
    app.run(debug=True)
