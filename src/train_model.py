# src/train_model.py

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def train_model():
    print("🔹 Loading training dataset...")

    df = pd.read_csv("data/processed/final_sip_training_dataset.csv")
    print(f"✅ Dataset loaded with shape: {df.shape}")

    # ===============================
    # 1. ENCODE CATEGORICAL FEATURES
    # ===============================
    categorical_cols = ['risk_appetite', 'fund_risk_category']

    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # ===============================
    # 2. SELECT FEATURES & TARGET
    # ===============================
    features = [
        'age',
        'monthly_allowance',
        'financial_literacy_score',
        'sip_amount',
        'fund_risk_score',
        'min_investment',
        'risk_appetite',
        'fund_risk_category'
    ]

    target = 'label'

    X = df[features]
    y = df[target]

    if y.dtype == 'object':
        y = LabelEncoder().fit_transform(y)

    # ===============================
    # 3. SPLIT DATA
    # ===============================
    print("📊 Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ===============================
    # 4. TRAIN MODEL
    # ===============================
    print("🤖 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # ===============================
    # 5. EVALUATION
    # ===============================
    y_pred = model.predict(X_test)
    print("✅ Training completed")
    print(f"🎯 Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

    # ===============================
    # 6. SAVE MODEL
    # ===============================
    joblib.dump(model, "models/sip_model.pkl")
    joblib.dump(encoders, "models/encoders.pkl")

    print("💾 Model & encoders saved successfully")

if __name__ == "__main__":
    train_model()
