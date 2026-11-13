# CYPHER – AI Phishing URL Detection Dashboard

CYPHER is a **machine learning powered phishing URL detection dashboard** that analyzes URLs using **lexical feature extraction** and **Random Forest classification**. The system provides real-time phishing detection along with interactive dashboard analytics.

---

## Project Overview

Phishing attacks are one of the most common cyber threats used to steal credentials, financial data, and sensitive information. This project detects phishing URLs using AI techniques and provides users with a dashboard to visualize detection results.

The project demonstrates an **end-to-end machine learning pipeline**, including:

- Data Collection  
- Feature Extraction  
- Model Training  
- Real-Time URL Detection  
- Dashboard Visualization  

---

## Technologies Used

### Backend
- Python  
- Flask  
- Scikit-Learn  
- Pandas  

### Frontend
- HTML5  
- CSS3  
- JavaScript  
- Chart.js  

### Machine Learning
- Random Forest Classifier  
- Lexical URL Feature Extraction  

---

## Machine Learning Pipeline

```
Data Collection → Pre-processing → Feature Extraction → Model Training → Detection → Dashboard Reporting
```

---

## Features

- Real-time phishing URL detection  
- Interactive dashboard analytics  
- Random Forest ML model  
- URL lexical feature extraction  
- Dynamic phishing statistics graph  
- Simple and responsive UI  
- Lightweight and fast processing  

---

## Feature Extraction

The model analyzes URLs using **8 lexical features**:

1. **URL Length** – Detects suspicious long URLs  
2. **Dot Count** – Multiple subdomains may indicate phishing  
3. **HTTPS Check** – Checks if secure protocol is used  
4. **Subdomain Length** – Long subdomains can be suspicious  
5. **Domain Length** – Abnormal domain length detection  
6. **Suffix Length** – TLD length analysis  
7. **Suspicious Keywords** – Detects words like login, verify, secure  
8. **Digit Presence** – Detects numbers inside URLs  

---

## Machine Learning Model

The system uses:

- **Random Forest Classifier**

### Why Random Forest?

- High accuracy on tabular data  
- Handles feature variations well  
- Resistant to overfitting  
- Fast training and prediction  

---

## Model Evaluation Metrics

- Accuracy  
- Precision  
- Recall  
- F1 Score  
- Confusion Matrix  

---

## Project Structure

```
CYPHER/
├── cypher/                    # Flask application
│   ├── app.py
│   ├── src/feature_extraction.py, train_model.py
│   ├── model/phishing_model.pkl
│   ├── data/urls_dataset.csv
│   ├── templates/             # HTML pages
│   ├── static/css/            # Versioned static assets (cached by CloudFront)
│   ├── tests/                 # pytest suite run by Jenkins
│   ├── requirements.txt
│   └── requirements-dev.txt
├── deploy/                    # EC2 setup, deploy + rollback scripts, AWS policies
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
├── DEVOPS.md
└── README.md
```

---

## Installation & Setup

### Option A — Docker (recommended)
```bash
git clone https://github.com/Devansh42-cyber/CYPHER.git
cd CYPHER
docker build -t cypher .
docker run -d --name cypher -p 5000:5000 --env-file .env.example cypher
```
Open http://localhost:5000 — health check: http://localhost:5000/health

### Option B — Local Python
```bash
git clone https://github.com/Devansh42-cyber/CYPHER.git
cd CYPHER/cypher
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements-dev.txt
python app.py
```

### Run Tests
```bash
cd cypher
python -m pytest -v
```

### Retrain the Model (optional)
```bash
cd cypher
python src/train_model.py
```

### Configuration (environment variables)
| Variable | Default | Purpose |
|---|---|---|
| `APP_ENV` | `development` | Environment name shown in the footer / health check |
| `APP_VERSION` | `dev` | Version label; set to the build tag by the pipeline |
| `PORT` | `5000` | Port the app listens on |
| `FLASK_DEBUG` | `0` | Set to `1` for Flask debug mode (local only) |

See [DEVOPS.md](DEVOPS.md) for the CI/CD pipeline and AWS deployment.

---

## Sample Usage

1. Enter URL in dashboard  
2. Click **"Check"**

### System Displays:
- Phishing / Legitimate result  
- Updates dashboard statistics  
- Updates dynamic graph  

---

## Dashboard Modules

- URL Scanner  
- Daily Detection Statistics  
- Model Performance Overview  
- Sandboxing External Link Testing  

---

## Limitations

- Uses lexical features only  
- Dataset size limited in prototype  
- Cannot detect advanced phishing that bypass URL pattern detection  
- Does not analyze webpage content or behavior  

---

## Future Improvements

- Content-based feature extraction  
- Deep learning model integration  
- WHOIS and DNS analysis  
- Real phishing dataset integration (PhishTank, OpenPhish)  
- User authentication and reporting  
- Threat intelligence API integration  

---

## Academic Purpose

This project was developed as part of a cybersecurity academic project to demonstrate practical application of AI in phishing detection.



---

## License

This project is for educational and research purposes only.
