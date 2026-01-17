import os
print("="*70)
print("FINAL PROJECT VALIDATION")
print("="*70)

# Check critical files
files = [
    'data/raw/mutual_funds_india.csv',
    'data/synthetic/teen_sip_dataset.csv', 
    'data/processed/final_sip_training_dataset.csv',
    'models/best_sip_model.pkl'
]

print("📁 Checking files:")
all_good = True
for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024
        print(f"✅ {f} ({size:.1f} KB)")
    else:
        print(f"❌ {f} - MISSING")
        all_good = False

# Check Python environment
print("\n🐍 Checking Python environment:")
try:
    import pandas, numpy, sklearn, joblib
    print("✅ All required packages installed")
except ImportError as e:
    print(f"❌ Missing package: {e}")
    all_good = False

print("\n" + "="*70)
if all_good:
    print("🎉 PROJECT IS READY FOR VIVA EVALUATION!")
    print("\n📋 For your presentation:")
    print("   1. Explain the dataset creation process")
    print("   2. Show model accuracy from training output")
    print("   3. Demonstrate predictions")
    print("   4. Discuss feature importance")
    print("   5. Highlight ethical considerations")
else:
    print("⚠️  Some issues found. Please fix before submission.")
print("="*70)