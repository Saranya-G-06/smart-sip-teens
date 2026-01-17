import os
import pandas as pd
import numpy as np

def print_header(text):
    print("\n" + "="*70)
    print(f"🔍 {text}")
    print("="*70)

def validate_project():
    """Validate the entire project structure and components"""
    
    print_header("SMART SIP RECOMMENDATION SYSTEM - FINAL PROJECT VALIDATION")
    
    validation_passed = True
    issues = []
    
    # 1. Validate Project Structure
    print_header("1. PROJECT STRUCTURE VALIDATION")
    
    required_dirs = [
        'data/raw',
        'data/synthetic',
        'data/processed',
        'docs',
        'src'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ - MISSING")
            issues.append(f"Missing directory: {directory}")
            validation_passed = False
    
    # 2. Check Required Files
    print_header("2. REQUIRED FILES CHECK")
    
    required_files = [
        ('data/raw/mutual_funds_india.csv', 'Raw mutual fund dataset'),
        ('data/synthetic/teen_sip_dataset.csv', 'Synthetic teen dataset'),
        ('data/processed/final_sip_training_dataset.csv', 'Final training dataset'),
        ('src/clean_mutual_fund_data.py', 'Data cleaning script'),
        ('src/train_model.py', 'Model training script')
    ]
    
    files_found = 0
    files_missing = 0
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {description}: {file_path} ({size:,} bytes)")
            files_found += 1
        else:
            print(f"❌ {description}: {file_path} - NOT FOUND")
            issues.append(f"Missing file: {file_path}")
            files_missing += 1
    
    print(f"\n📊 Files Status: {files_found} found, {files_missing} missing")
    
    # 3. Check Python Environment
    print_header("3. PYTHON ENVIRONMENT CHECK")
    
    try:
        import pandas
        import numpy
        import sklearn
        import matplotlib
        
        print("✅ Required packages are installed")
        print(f"   Pandas v{pandas.__version__}")
        print(f"   NumPy v{numpy.__version__}")
        print(f"   Scikit-learn v{sklearn.__version__}")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        issues.append(f"Missing Python package: {e}")
        validation_passed = False
    
    # 4. Check Data Quality
    print_header("4. DATA QUALITY CHECK")
    
    # Check if training dataset exists and is valid
    training_file = 'data/processed/final_sip_training_dataset.csv'
    if os.path.exists(training_file):
        try:
            df = pd.read_csv(training_file)
            print(f"✅ Training dataset loaded successfully")
            print(f"   Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            print(f"   Columns: {', '.join(df.columns.tolist())}")
            
            # Check for missing values
            missing_values = df.isnull().sum().sum()
            if missing_values == 0:
                print(f"✅ No missing values in dataset")
            else:
                print(f"⚠️  Found {missing_values} missing values")
            
            # Check target column
            if 'label' in df.columns:
                target_dist = df['label'].value_counts()
                print(f"✅ Target variable 'label' found")
                print(f"   Class distribution: {dict(target_dist)}")
                print(f"   Class ratio: {target_dist.get(0, 0)}:1 vs {target_dist.get(1, 0)}:0")
            else:
                print("❌ Target column 'label' not found in dataset")
                issues.append("Missing 'label' column in training data")
                validation_passed = False
                
        except Exception as e:
            print(f"❌ Error loading training dataset: {e}")
            issues.append(f"Dataset error: {e}")
            validation_passed = False
    else:
        print("⚠️  Training dataset not found - run data processing scripts first")
    
    # 5. Check Model Files
    print_header("5. MODEL FILES CHECK")
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
        print("📁 Created 'models/' directory")
    
    model_files = ['models/best_sip_model.pkl', 'models/scaler.pkl']
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"✅ Model file exists: {model_file}")
        else:
            print(f"⚠️  Model file missing: {model_file}")
            print(f"   Run: python src/train_model.py to generate model files")
    
    # 6. Final Summary
    print_header("PROJECT VALIDATION SUMMARY")
    
    if validation_passed and files_missing == 0:
        print("🎉" + "="*68 + "🎉")
        print("✅ PROJECT IS READY FOR EVALUATION!")
        print("🎉" + "="*68 + "🎉")
        
        print("\n📋 Your project contains:")
        print("   ✓ Complete folder structure")
        print("   ✓ All required data files")
        print("   ✓ Cleaned and processed datasets")
        print("   ✓ Python environment with required packages")
        print("   ✓ Valid training dataset with target variable")
        
        print("\n🚀 NEXT STEPS FOR VIVA:")
        print("   1. Train your model: python src/train_model.py")
        print("   2. Test predictions: python src/predict_sip.py")
        print("   3. Create presentation slides in docs/ folder")
        print("   4. Practice explaining your approach")
        
        return True
    else:
        print("⚠️" + "="*68 + "⚠️")
        print("PROJECT REQUIRES ATTENTION")
        print("⚠️" + "="*68 + "⚠️")
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Directories: {sum(os.path.exists(d) for d in required_dirs)}/{len(required_dirs)}")
        print(f"   ✅ Files: {files_found}/{len(required_files)}")
        print(f"   ✅ Python packages: {'All installed' if validation_passed else 'Missing'}")
        
        if issues:
            print(f"\n❌ Issues to fix:")
            for issue in issues:
                print(f"   • {issue}")
        
        print(f"\n🔧 IMMEDIATE ACTIONS REQUIRED:")
        print("   1. Check that mutual_funds_india.csv is in data/raw/")
        print("   2. Run data cleaning: python src/clean_mutual_fund_data.py")
        print("   3. Generate synthetic data (if needed)")
        print("   4. Merge datasets to create final training dataset")
        
        return False

if __name__ == "__main__":
    success = validate_project()
    
    # Provide next steps based on validation
    if not success:
        print("\n📋 QUICK FIX CHECKLIST:")
        print("="*70)
        
        # Check for raw data
        if not os.path.exists('data/raw/mutual_funds_india.csv'):
            print("❌ Step 1: Download mutual_funds_india.csv to data/raw/")
        else:
            print("✅ Step 1: Raw data exists")
        
        # Check for synthetic data
        if not os.path.exists('data/synthetic/teen_sip_dataset.csv'):
            print("❌ Step 2: Generate synthetic data using:")
            print("   python src/generate_synthetic_data.py")
        else:
            print("✅ Step 2: Synthetic data exists")
        
        # Check for processed data
        if not os.path.exists('data/processed/final_sip_training_dataset.csv'):
            print("❌ Step 3: Process and merge datasets")
            print("   Run your data merging script")
        else:
            print("✅ Step 3: Training dataset exists")
        
        print("\n💡 Tip: If you're stuck, check your existing scripts in src/ folder")