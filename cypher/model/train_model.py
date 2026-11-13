import pandas as pd
import joblib
import re
import tldextract
from sklearn.ensemble import RandomForestClassifier

# ---------------------------
# SAME FEATURE FUNCTION AS FLASK
# ---------------------------
def extract_features(url):
    ext = tldextract.extract(url)

    return [
        len(url),                                      # 1
        url.count('.'),                                # 2
        int(url.startswith("https")),                  # 3
        len(ext.subdomain),                            # 4
        len(ext.domain),                               # 5
        len(ext.suffix),                               # 6
       int(any(token in url.lower() for token in [
    "login", "signin", "verify", "update", "confirm",
    "secure", "account", "bank", "payment", "invoice",
    "webscr", "authenticate", "validate", "reset",
    "default.aspx", "paginas", "smiles"
]))
,                  # 7
        int(re.search(r'\d', url) is not None)         # 8
    ]

# ---------------------------
# SIMPLE TRAINING DATA
# ---------------------------
data = {
    "url": [
        "https://google.com",
        "https://amazon.com",
        "https://github.com",
        "http://paypal-login-security-check.com",
        "https://secure-login-bank.com/account",
        "http://verify-update-paypal.com",
        "http://freebonus1000.ru/login",
        "https://microsoft.com"
    ],
    "label": [0, 0, 0, 1, 1, 1, 1, 0]
}

df = pd.DataFrame(data)
df["features"] = df["url"].apply(extract_features)

X = df["features"].tolist()
y = df["label"].tolist()

# ---------------------------
# TRAIN MODEL
# ---------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# ---------------------------
# SAVE MODEL
# ---------------------------
joblib.dump(model, "phishing_model.pkl")
print("✔ Model saved as phishing_model.pkl (8 features)")
