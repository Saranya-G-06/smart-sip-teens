# 💰 Smart SIP for Teens

A gamified, ML-powered platform that helps teenagers develop early investment habits through SIP simulation and financial education.

## 🚀 Features

- **AI-Powered SIP Recommendation** — RandomForest ML model with SHAP explainability
- **Interactive SIP Simulator** — Compound interest calculator with Plotly charts
- **AI Financial Advisor Chatbot** — Rule-based chatbot for financial questions
- **Gamification System** — Points, badges, levels, and daily streaks
- **Financial Education Hub** — 8 lessons with reward points
- **PDF Report Generator** — Downloadable personalized investment reports
- **Secure Auth** — Password hashing, session management, SQLite storage

## 🛠️ Tech Stack

Python · Streamlit · Scikit-learn · Pandas · NumPy · Plotly · SQLite · SHAP · ReportLab

## 📦 Installation

```bash
git clone https://github.com/yourusername/SmartSIP_Teens.git
cd SmartSIP_Teens
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Streamlit Cloud Deployment

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `app.py`
5. Click **Deploy**

## 🎮 Demo

- **Username:** `demo`
- **Password:** `demo123`

## 📁 Project Structure

```
SmartSIP_Teens/
├── app.py                    # Main entry point
├── requirements.txt
├── README.md
├── data/
│   ├── teen_finance_dataset.csv   # 3200 rows for ML training
│   ├── mutual_funds.csv           # 55 mutual funds
│   ├── financial_lessons.csv      # 8 lessons
│   └── sample_users.csv
├── models/                   # Auto-generated on first run
├── database/                 # SQLite (auto-created)
├── utils/
│   ├── auth.py              # Login/signup/streak
│   ├── database.py          # DB setup
│   ├── sip_calculator.py    # SIP math
│   ├── ml_model.py          # ML + SHAP
│   ├── chatbot.py           # Rule-based chatbot
│   └── gamification.py      # Points/badges
└── pages/
    ├── dashboard.py
    ├── sip_simulator.py
    ├── advisor.py
    ├── education.py
    ├── gamification_page.py
    └── report.py
```

## 📖 License

MIT License — Free to use and modify.
