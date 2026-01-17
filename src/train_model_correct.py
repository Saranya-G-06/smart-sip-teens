import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

print("🤖 SMART SIP RECOMMENDATION SYSTEM - FINAL TRAINING")
print("="*70)

# Load the dataset
df = pd.read_csv('data/processed/final_sip_training_dataset.csv')
print(f"✅ Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
print(f"Columns: {df.columns.tolist()}")

# Drop non-numeric or unnecessary columns
# 'fund_name' contains 'Unknown' strings - we need to handle or drop it
if 'fund_name' in df.columns:
    print(f"⚠️  Dropping 'fund_name' column (contains string values)")
    df = df.drop('fund_name', axis=1)

# Check data types
print(f"\n📊 Data types:")
print(df.dtypes)

# Identify categorical columns
categorical_cols = []
for col in df.columns:
    if df[col].dtype == 'object' and col != 'label':
        categorical_cols.append(col)
        print(f"Categorical: {col} - Unique values: {df[col].unique()[:5]}...")

print(f"\n🎯 Target distribution:")
print(df['label'].value_counts())
print(f"Recommended: {df['label'].sum()}, Not Recommended: {len(df) - df['label'].sum()}")

# Encode categorical variables
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
    print(f"Encoded '{col}' with {len(le.classes_)} unique values")

# Prepare features and target
X = df.drop('label', axis=1)
y = df['label']

print(f"\n📊 Final feature set ({X.shape[1]} features): {X.columns.tolist()}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📈 Data split:")
print(f"Training: {X_train.shape[0]} samples")
print(f"Testing: {X_test.shape[0]} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✅ Features scaled")

# Train models
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

print(f"\n🚀 Training models...")
results = {}
best_accuracy = 0
best_model_name = ""

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'y_pred': y_pred
    }
    
    print(f"  Accuracy: {accuracy:.2%}")
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model_name = name

# Select best model
best_model = results[best_model_name]['model']
print(f"\n🏆 Best Model: {best_model_name} (Accuracy: {best_accuracy:.2%})")

# Save model artifacts
os.makedirs('models', exist_ok=True)
joblib.dump(best_model, 'models/best_sip_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(label_encoders, 'models/label_encoders.pkl')
joblib.dump(list(X.columns), 'models/feature_names.pkl')

print(f"\n💾 Model saved: models/best_sip_model.pkl")
print(f"   Scaler saved: models/scaler.pkl")
print(f"   Encoders saved: models/label_encoders.pkl")
print(f"   Feature names saved: models/feature_names.pkl")

# Generate evaluation report
print(f"\n📋 Evaluation Report:")
y_pred_best = results[best_model_name]['y_pred']
print(classification_report(y_test, y_pred_best, target_names=['Not Recommended', 'Recommended']))

# Create confusion matrix
cm = confusion_matrix(y_test, y_pred_best)
os.makedirs('docs', exist_ok=True)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title(f'Confusion Matrix - {best_model_name}\nAccuracy: {best_accuracy:.2%}')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('docs/confusion_matrix.png')
print("✅ Confusion matrix saved: docs/confusion_matrix.png")

# Feature importance
if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🔑 Feature Importance:")
    print(feature_importance.to_string(index=False))
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title('Feature Importance for SIP Recommendation')
    plt.tight_layout()
    plt.savefig('docs/feature_importance.png')
    print("✅ Feature importance plot saved: docs/feature_importance.png")

print(f"\n" + "="*70)
print("🎉 MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("="*70)