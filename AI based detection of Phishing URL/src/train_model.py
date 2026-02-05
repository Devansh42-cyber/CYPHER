# src/train_model.py
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from feature_extraction import extract_features

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'data')
MODEL_DIR = os.path.join(ROOT, 'model')
DATA_CSV = os.path.join(DATA_DIR, 'urls_dataset.csv')
MODEL_FILE = os.path.join(MODEL_DIR, 'phishing_model.pkl')

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

def load_dataset(path=DATA_CSV):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No dataset found at {path}. Create data/urls_dataset.csv or run sample generator.")
    df = pd.read_csv(path)
    if 'url' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'url' and 'label' columns (label: 1=phish, 0=legit)")
    df = df.dropna(subset=['url'])
    # Normalize textual labels
    df['label'] = df['label'].apply(lambda x: 1 if str(x).strip().lower() in ['1','phish','phishing','malicious','true','yes'] else 0)
    return df

def build_features(urls):
    return np.array([extract_features(u) for u in urls])

def main():
    ensure_dirs()
    df = load_dataset()
    X = build_features(df['url'].values)
    y = df['label'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    print("Confusion matrix:\n", confusion_matrix(y_test, preds))

    joblib.dump(clf, MODEL_FILE)
    print("Saved model to:", MODEL_FILE)

if __name__ == "__main__":
    main()
