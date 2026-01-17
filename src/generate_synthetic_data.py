import pandas as pd
import numpy as np

print("🔧 Generating Synthetic Teen Financial Dataset...")

# Set random seed for reproducibility
np.random.seed(42)

# Number of synthetic teen profiles
n_samples = 1000

# Generate synthetic teen data
data = {
    'age': np.random.randint(13, 20, n_samples),
    'monthly_allowance': np.random.randint(500, 5000, n_samples),
    'financial_literacy_score': np.random.uniform(1, 10, n_samples).round(1),
    'risk_appetite': np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.4, 0.4, 0.2]),
    'saving_habit': np.random.choice(['Saver', 'Balanced', 'Spender'], n_samples, p=[0.3, 0.5, 0.2]),
    'financial_goals': np.random.choice(['Education', 'Gadget', 'Travel', 'Emergency Fund'], n_samples),
    'parental_guidance': np.random.choice(['Yes', 'No'], n_samples, p=[0.7, 0.3])
}

df = pd.DataFrame(data)

# Add SIP amount based on rules
def calculate_sip_amount(row):
    base_amount = row['monthly_allowance'] * np.random.uniform(0.1, 0.3)
    
    # Adjust based on saving habit
    if row['saving_habit'] == 'Saver':
        base_amount *= 1.2
    elif row['saving_habit'] == 'Spender':
        base_amount *= 0.8
    
    # Adjust based on financial literacy
    base_amount *= (row['financial_literacy_score'] / 10)
    
    return round(base_amount, -2)  # Round to nearest 100

df['sip_amount'] = df.apply(calculate_sip_amount, axis=1)

# Add fund category based on risk appetite
def assign_fund_category(row):
    if row['risk_appetite'] == 'Low':
        return np.random.choice(['Debt', 'Liquid'], p=[0.7, 0.3])
    elif row['risk_appetite'] == 'Medium':
        return np.random.choice(['Hybrid', 'Balanced', 'Index'], p=[0.5, 0.3, 0.2])
    else:  # High
        return np.random.choice(['Equity', 'Sectoral', 'Small Cap'], p=[0.6, 0.3, 0.1])

df['fund_category'] = df.apply(assign_fund_category, axis=1)

# Add fund risk category
risk_mapping = {
    'Debt': 'Low', 'Liquid': 'Low',
    'Hybrid': 'Medium', 'Balanced': 'Medium', 'Index': 'Medium',
    'Equity': 'High', 'Sectoral': 'High', 'Small Cap': 'High'
}
df['fund_risk_category'] = df['fund_category'].map(risk_mapping)

# Add label (target variable) based on logical rules
def assign_label(row):
    # Rules for recommendation
    if row['age'] < 16 and row['risk_appetite'] == 'High':
        return 0  # Not recommended (too young for high risk)
    elif row['sip_amount'] > row['monthly_allowance'] * 0.5:
        return 0  # Not recommended (SIP too high)
    elif row['financial_literacy_score'] < 3:
        return 0  # Not recommended (low financial literacy)
    elif row['risk_appetite'] == 'Low' and row['fund_risk_category'] == 'High':
        return 0  # Not recommended (risk mismatch)
    else:
        return 1  # Recommended

df['label'] = df.apply(assign_label, axis=1)

# Save to CSV
output_path = 'data/synthetic/teen_sip_dataset.csv'
df.to_csv(output_path, index=False)

print(f"✅ Generated {n_samples} synthetic teen profiles")
print(f"✅ Saved to: {output_path}")
print(f"✅ Dataset shape: {df.shape}")
print(f"\n📊 Dataset Overview:")
print(df.head())
print(f"\n📈 Label Distribution:")
print(df['label'].value_counts())
print(f"   Recommended (1): {(df['label'].sum() / len(df) * 100):.1f}%")
print(f"   Not Recommended (0): {((len(df) - df['label'].sum()) / len(df) * 100):.1f}%")