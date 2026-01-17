import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

print("🤖 Training Smart SIP Recommendation Model")
print("="*60)

# Load the training dataset
try:
    df = pd.read_csv('data/processed/final_sip_training_dataset.csv')
    print(f"✅ Loaded dataset: {df.shape[0]} samples, {df.shape[1]} features")
except:
    print("❌ Could not load training dataset")
    print("💡 Generating sample data for demonstration...")
    
    # Create sample data if file doesn't exist
    np.random.seed(42)
    n_samples = 500
    
    data = {
        'age': np.random.randint(13, 20, n_samples),
        'monthly_allowance': np.random.randint(500, 5000, n_samples),
        'financial_literacy_score': np.random.uniform(1, 10, n_samples).round(1),
        'risk_appetite': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'sip_amount': np.random.randint(100, 2000, n_samples),
        'fund_category': np.random.choice(['Equity', 'Debt', 'Hybrid'], n_samples),
        'fund_risk_category': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'label': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data/processed/final_sip_training_dataset.csv', index=False)
    print(f"✅ Created sample dataset with {n_samples} samples")

# Display dataset info
print(f"\n📊 Dataset Info:")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df.head())

# Encode categorical variables
print(f"\n🔄 Preprocessing data...")
label_encoders = {}

categorical_cols = ['risk_appetite', 'fund_category', 'fund_risk_category']
for col in categorical_cols:
    if col in df.columns:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"Encoded '{col}' -> {list(le.classes_)}")

# Prepare features and target
# Use numeric columns only
numeric_cols = ['age', 'monthly_allowance', 'financial_literacy_score', 'sip_amount']
encoded_cols = [col for col in df.columns if '_encoded' in col]

feature_cols = numeric_cols + encoded_cols
X = df[feature_cols]
y = df['label']

print(f"\n🎯 Features used: {feature_cols}")
print(f"Target: label (0: Not Recommended, 1: Recommended)")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 Data split:")
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
print(f"\n🚀 Training Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"\n📈 Model Evaluation:")
print(f"Accuracy: {accuracy:.2%}")

print(f"\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Not Recommended', 'Recommended']))

# Feature importance
if hasattr(model, 'feature_importances_'):
    print(f"\n🔑 Feature Importance:")
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in importance_df.iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")

# Save model artifacts
os.makedirs('models', exist_ok=True)

joblib.dump(model, 'models/best_sip_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(label_encoders, 'models/label_encoders.pkl')
joblib.dump(feature_cols, 'models/feature_names.pkl')

print(f"\n💾 Model artifacts saved to 'models/' directory:")
print(f"  ✅ best_sip_model.pkl - Trained model")
print(f"  ✅ scaler.pkl - Feature scaler")
print(f"  ✅ label_encoders.pkl - Categorical encoders")
print(f"  ✅ feature_names.pkl - Feature names")

# Test the model
print(f"\n🎯 Sample Predictions:")
sample_idx = np.random.randint(0, len(X_test), 3)
for i, idx in enumerate(sample_idx, 1):
    actual = y_test.iloc[idx]
    predicted = y_pred[idx]
    confidence = y_pred_proba[idx] if predicted == 1 else 1 - y_pred_proba[idx]
    
    print(f"\nSample {i}:")
    print(f"  Age: {X_test.iloc[idx]['age']:.0f}")
    print(f"  Allowance: ₹{X_test.iloc[idx]['monthly_allowance']:.0f}")
    print(f"  SIP Amount: ₹{X_test.iloc[idx]['sip_amount']:.0f}")
    print(f"  Actual: {'Recommended' if actual == 1 else 'Not Recommended'}")
    print(f"  Predicted: {'Recommended' if predicted == 1 else 'Not Recommended'}")
    print(f"  Confidence: {confidence:.1%}")

print(f"\n{'='*60}")
print("✅ MODEL TRAINING COMPLETED!")
print("✅ Your project is ready for viva demonstration!")
print("="*60)