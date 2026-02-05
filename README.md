CYPHER – AI Phishing URL Detection Dashboard
CYPHER is a machine learning powered phishing URL detection dashboard that analyses URLs using lexical feature extraction and Random Forest classification. The system provides real-time phishing detection along with interactive dashboard analytics.


Project Overview
Phishing attacks are one of the most common cyber threats used to steal credentials, financial data, and sensitive information. This project detects phishing URLs using AI techniques and provides users with a dashboard to visualize detection results.

The project demonstrates an end-to-end machine learning pipeline including:
-Data Collection
-Feature Extraction
-Model Training
-Real-Time URL Detection
-Dashboard Visualization

Technologies Used
Backend
-Python
-Flask
-Scikit-Learn
-Pandas


Frontend
-HTML5
-CSS3
-JavaScript
-Chart.js

*Machine Learning:
Random Forest Classifier
Lexical URL Feature Extraction


* Machine Learning Pipeline
Data Collection → Pre-processing → Feature Extraction → Model Training → Detection → Dashboard Reporting

*Features
Real-time phishing URL detection
Interactive dashboard analytics
Random Forest ML model
URL lexical feature extraction
Dynamic phishing statistics graph
Simple and responsive UI
Lightweight and fast processing

*Feature Extraction
The model analyses URLs using 8 lexical features:
URL Length--Detects suspicious long URLs
Dot Count--Multiple subdomains may indicate phishing
HTTPS Check--Checks if secure protocol is used
Subdomain Length--Long subdomains can be suspicious
Domain Length--Abnormal domain length detection
Suffix Length--TLD length analysis
Suspicious Keywords--Detects words like login, verify, secure
Digit Presence--Detects numbers inside URLs

*Machine Learning Model
The system uses:
Random Forest Classifier

*Why Random Forest?
High accuracy on tabular data
Handles feature variations well
Resistant to overfitting
Fast training and prediction

*Model Evaluation Metrics
Accuracy
Precision
Recall
F1 Score
Confusion Matrix

*Project Structure
CYPHER
│
├── app.py
├── model/
│     └── phishing_model.pkl
├── src/
│     └── feature_extraction.py
├── data/
│     └── urls_dataset.csv
├── templates/
│     ├── index.html
│     ├── Loading.html
│     ├── About.html
│     └── Contact.html
├── static/
│
└── README.md

**Installation & Setup
*Clone Repository
git clone https://github.com/yourusername/cypher-phishing-detector.git
cd cypher-phishing-detector

*Create Virtual Environment
python -m venv venv
venv\Scripts\activate

*Install Dependencies
pip install -r requirements.txt

*Train Model
python src/train_model.py

*Run Application
python app.py

*Open Dashboard
http://127.0.0.1:5000

*Sample Usage
Enter URL in dashboard
Click "Check"

*System displays:
Phishing / Legitimate result
Updates dashboard statistics
Updates dynamic graph

*Dashboard Modules
URL Scanner
Daily Detection Statistics
Model Performance Overview
Sandboxing External Link Testing

*Limitations
Uses lexical features only
Dataset size limited in prototype
Cannot detect advanced phishing that bypass URL pattern detection
Does not analyze webpage content or behavior

*Future Improvements

Content-based feature extraction
Deep learning model integration
WHOIS and DNS analysis
Real phishing dataset integration (PhishTank, OpenPhish)
User authentication and reporting
Threat intelligence API integration

*Academic Purpose
This project was developed as part of a cybersecurity academic project to demonstrate practical application of AI in phishing detection.

*Author
Devansh Baluni
Cybersecurity Student
Interested in AI Security, Threat Detection, and Blue Team Operations

*License
This project is for educational and research purposes only.
