import os
import pandas as pd

BASE_DIR = os.getcwd()
errors_found = False

REQUIRED_FOLDERS = ["data", "docs", "notebooks", "src", "tests"]

REQUIRED_DATA_FILES = [
    "teen_sip_dataset.csv",
    "mutual_funds_india.csv",
    "cleaned_mutual_funds.csv",
    "final_sip_training_dataset.csv"
]

REQUIRED_SRC_FILES = [
    "data_preprocessing.py",
    "clean_mutual_fund_data.py",
    "merge_teen_fund_data.py",
    "train_model.py"
]

def check_folders():
    global errors_found
    print("\n📁 Checking folder structure...")
    for folder in REQUIRED_FOLDERS:
        if os.path.isdir(folder):
            print(f"✅ Folder exists: {folder}")
        else:
            print(f"❌ Missing folder: {folder}")
            errors_found = True

def check_files(folder, files):
    global errors_found
    print(f"\n📄 Checking files in '{folder}/'...")
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            errors_found = True

def check_csv_content():
    global errors_found
    print("\n📊 Validating CSV content...")
    try:
        teen_df = pd.read_csv("data/teen_sip_dataset.csv")
        final_df = pd.read_csv("data/final_sip_training_dataset.csv")

        teen_cols = {
            "age", "monthly_allowance",
            "risk_tolerance", "savings_consistency"
        }

        final_cols = {
            "age", "monthly_allowance", "risk_tolerance",
            "scheme_name", "returns_1yr", "returns_3yr",
            "recommended_sip"
        }

        if teen_cols.issubset(teen_df.columns):
            print("✅ Teen dataset columns OK")
        else:
            print("❌ Teen dataset columns missing")
            errors_found = True

        if final_cols.issubset(final_df.columns):
            print("✅ Final dataset columns OK")
        else:
            print("❌ Final dataset columns missing")
            errors_found = True

        if teen_df.isnull().sum().sum() == 0:
            print("✅ Teen dataset has no missing values")
        else:
            print("⚠️ Teen dataset has missing values")

        if final_df.isnull().sum().sum() == 0:
            print("✅ Final dataset has no missing values")
        else:
            print("⚠️ Final dataset has missing values")

    except Exception as e:
        print(f"❌ CSV validation failed: {e}")
        errors_found = True

def final_summary():
    print("\n==============================")
    print("📌 PROJECT VALIDATION SUMMARY")
    print("==============================")
    if errors_found:
        print("❌ Project is NOT ready for evaluation")
        print("➡️ Missing files/modules detected")
    else:
        print("✅ Project is READY for evaluation")
    print("==============================\n")

if __name__ == "__main__":
    print("\n🔍 SMART SIP TEENS – PROJECT VALIDATION STARTED")
    check_folders()
    check_files("data", REQUIRED_DATA_FILES)
    check_files("src", REQUIRED_SRC_FILES)
    check_csv_content()
    final_summary()
