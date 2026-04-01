import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib, os

df = pd.read_csv('/home/claude/SmartSIP_Teens/data/teen_finance_dataset.csv')
le = LabelEncoder()
df['risk_tolerance_enc'] = le.fit_transform(df['risk_tolerance'])

features = ['age', 'monthly_allowance', 'savings_rate', 'financial_literacy_score', 'investment_horizon', 'risk_tolerance_enc']
X = df[features]
y = df['recommended_sip']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
print(f"R2: {r2_score(y_test, preds):.4f}")

os.makedirs('/home/claude/SmartSIP_Teens/models', exist_ok=True)
joblib.dump({'model': model, 'label_encoder': le, 'features': features}, '/home/claude/SmartSIP_Teens/models/sip_recommendation_model.pkl')
print("Model saved!")
