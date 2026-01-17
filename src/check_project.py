import os
import pandas as pd

print("="*70)
print("SMART SIP TEENS - PROJECT STATUS CHECK")
print("="*70)

# Check folders
print("\n📁 FOLDER STRUCTURE:")
folders = ['data/raw', 'data/synthetic', 'data/processed', 'models', 'docs', 'src']
for folder in folders:
    if os.path.exists(folder):
        print(f"✅ {folder}/")
    else:
        print(f"❌ {folder}/")

# Check data files
print("\n📄 DATA FILES:")
files_to_check = [
    ('data/raw/mutual_funds_india.csv', 'Raw mutual fund data'),
    ('data/synthetic/teen_sip_dataset.csv', 'Synthetic teen data'),
    ('data/processed/cleaned_mutual_funds.csv', 'Cleaned mutual funds'),
    ('data/processed/final_sip_training_dataset.csv', 'Final training dataset')
]

for file_path, description in files_to_check:
    if os.path.exists(file_path):
        size_kb = os.path.getsize(file_path) / 1024
        print(f"✅ {description}: {file_path} ({size_kb:.1f} KB)")
    else:
        print(f"❌ {description}: {file_path} - MISSING")

# Check model files
print("\n🤖 MODEL FILES:")
model_files = ['models/best_sip_model.pkl', 'models/scaler.pkl']
for model_file in model_files:
    if os.path.exists(model_file):
        print(f"✅ {model_file}")
    else:
        print(f"❌ {model_file} - Run training script to create")

# Analyze training data
print("\n📊 TRAINING DATA ANALYSIS:")
training_file = 'data/processed/final_sip_training_dataset.csv'
if os.path.exists(training_file):
    try:
        df = pd.read_csv(training_file)
        print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"   Target distribution: {dict(df['label'].value_counts())}")
        
        # Check for required columns
        required_cols = ['age', 'monthly_allowance', 'financial_literacy_score', 
                        'risk_appetite', 'sip_amount', 'fund_category', 
                        'fund_risk_category', 'label']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
        else:
            print("✅ All required columns present")
            
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
else:
    print("❌ Training dataset not found")

# Final status
print("\n" + "="*70)
print("PROJECT STATUS SUMMARY:")
print("="*70)

# Count successes
files_exist = sum(os.path.exists(f[0]) for f in files_to_check)
folders_exist = sum(os.path.exists(f) for f in folders)

if files_exist == len(files_to_check) and folders_exist == len(folders):
    print("🎉 PROJECT IS READY FOR TRAINING!")
    print("\nNext step: Run -> python src\\train_model_fixed.py")
else:
    print("⚠️  PROJECT NEEDS ATTENTION")
    print(f"   Files: {files_exist}/{len(files_to_check)} found")
    print(f"   Folders: {folders_exist}/{len(folders)} found")
    print("\nRun the missing file scripts from src/ folder")

print("="*70)