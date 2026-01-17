import pandas as pd
import os

INPUT_FILE = os.path.join("data", "raw", "mutual_funds_india.csv")
OUTPUT_FILE = os.path.join("data", "processed", "cleaned_mutual_funds.csv")

# Possible column names used in mutual fund datasets
POSSIBLE_TYPE_COLUMNS = [
    "fund_type",
    "scheme_type",
    "scheme_category",
    "category",
    "asset_class"
]

def detect_fund_type_column(df):
    for col in POSSIBLE_TYPE_COLUMNS:
        if col in df.columns:
            return col
    return None

def assign_risk_category(value):
    if isinstance(value, str):
        v = value.lower()
        if "equity" in v:
            return 5
        elif "hybrid" in v:
            return 3
        elif "debt" in v:
            return 1
    return 3  # default medium risk

def clean_mutual_fund_data():
    print("🔹 Loading mutual fund dataset...")
    df = pd.read_csv(INPUT_FILE)

    df = df.drop_duplicates()
    df = df.dropna()

    fund_type_col = detect_fund_type_column(df)

    if fund_type_col is None:
        print("⚠ No fund type column found. Assigning medium risk to all funds.")
        df["risk_category"] = 3
    else:
        print(f"✅ Using '{fund_type_col}' as fund type column")
        df["risk_category"] = df[fund_type_col].apply(assign_risk_category)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("✅ Mutual fund data cleaned and saved to", OUTPUT_FILE)

if __name__ == "__main__":
    clean_mutual_fund_data()
