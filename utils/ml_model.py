import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

MODEL_PATH = "models/sip_recommendation_model.pkl"

def train_model():
    os.makedirs("models", exist_ok=True)
    df = pd.read_csv("data/teen_finance_dataset.csv")
    le = LabelEncoder()
    df["risk_encoded"] = le.fit_transform(df["risk_tolerance"])
    features = ["age", "monthly_allowance", "savings_rate", "financial_literacy_score", "investment_horizon", "risk_encoded"]
    X = df[features]
    y = df["recommended_sip"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump({"model": model, "label_encoder": le, "features": features}, MODEL_PATH)
    score = model.score(X_test, y_test)
    return model, score

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)

def predict_sip(age, monthly_allowance, savings_rate, financial_literacy_score, investment_horizon, risk_tolerance):
    data = load_model()
    model = data["model"]
    le = data["label_encoder"]
    risk_enc = le.transform([risk_tolerance])[0]
    features = np.array([[age, monthly_allowance, savings_rate, financial_literacy_score, investment_horizon, risk_enc]])
    prediction = model.predict(features)[0]
    return round(max(100, prediction), 0)

def get_shap_explanation(age, monthly_allowance, savings_rate, financial_literacy_score, investment_horizon, risk_tolerance):
    try:
        import shap
        data = load_model()
        model = data["model"]
        le = data["label_encoder"]
        risk_enc = le.transform([risk_tolerance])[0]
        X = np.array([[age, monthly_allowance, savings_rate, financial_literacy_score, investment_horizon, risk_enc]])
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)[0]
        feature_names = ["Age", "Monthly Allowance", "Savings Rate", "Financial Literacy", "Investment Horizon", "Risk Tolerance"]
        pairs = sorted(zip(feature_names, shap_values), key=lambda x: abs(x[1]), reverse=True)
        return pairs
    except Exception:
        return []
