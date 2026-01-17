import pandas as pd
import numpy as np

print("🔄 Merging Teen Data with Mutual Fund Data...")

# Load datasets
try:
    # Load synthetic teen data
    teen_df = pd.read_csv('data/synthetic/teen_sip_dataset.csv')
    print(f"✅ Loaded teen data: {teen_df.shape[0]} rows, {teen_df.shape[1]} columns")
    
    # Try to load cleaned mutual fund data
    try:
        fund_df = pd.read_csv('data/processed/cleaned_mutual_funds.csv')
        print(f"✅ Loaded mutual fund data: {fund_df.shape[0]} rows, {fund_df.shape[1]} columns")
    except:
        print("⚠️  No cleaned mutual fund data found, using synthetic data only")
        fund_df = None
    
    # If we have both datasets, merge them
    if fund_df is not None:
        # For each teen, assign a fund from the mutual fund dataset
        merged_rows = []
        
        for idx, teen in teen_df.iterrows():
            # Filter funds based on teen's fund category
            compatible_funds = fund_df[fund_df['category'] == teen['fund_category']]
            
            if len(compatible_funds) > 0:
                # Select a random compatible fund
                selected_fund = compatible_funds.sample(n=1).iloc[0]
                
                # Create merged row
                merged_row = {
                    'age': teen['age'],
                    'monthly_allowance': teen['monthly_allowance'],
                    'financial_literacy_score': teen['financial_literacy_score'],
                    'risk_appetite': teen['risk_appetite'],
                    'sip_amount': teen['sip_amount'],
                    'fund_category': teen['fund_category'],
                    'fund_risk_category': teen['fund_risk_category'],
                    'fund_name': selected_fund.get('fund_name', 'Unknown'),
                    'fund_risk_score': selected_fund.get('risk_score', 2.5),
                    'min_investment': selected_fund.get('min_sip_amount', 500),
                    'label': teen['label']
                }
                merged_rows.append(merged_row)
            else:
                # If no compatible fund, use teen data as is
                merged_row = {
                    'age': teen['age'],
                    'monthly_allowance': teen['monthly_allowance'],
                    'financial_literacy_score': teen['financial_literacy_score'],
                    'risk_appetite': teen['risk_appetite'],
                    'sip_amount': teen['sip_amount'],
                    'fund_category': teen['fund_category'],
                    'fund_risk_category': teen['fund_risk_category'],
                    'fund_name': 'Generic ' + teen['fund_category'] + ' Fund',
                    'fund_risk_score': 2.5,
                    'min_investment': 500,
                    'label': teen['label']
                }
                merged_rows.append(merged_row)
        
        final_df = pd.DataFrame(merged_rows)
    else:
        # Use only teen data (simplified version)
        final_df = teen_df.copy()
        if 'fund_name' not in final_df.columns:
            final_df['fund_name'] = 'Generic ' + final_df['fund_category'] + ' Fund'
        if 'fund_risk_score' not in final_df.columns:
            final_df['fund_risk_score'] = final_df['fund_risk_category'].map({'Low': 1, 'Medium': 2, 'High': 3})
        if 'min_investment' not in final_df.columns:
            final_df['min_investment'] = 500
    
    # Save the merged dataset
    output_path = 'data/processed/final_sip_training_dataset.csv'
    final_df.to_csv(output_path, index=False)
    
    print(f"\n✅ Merged dataset created: {final_df.shape[0]} rows, {final_df.shape[1]} columns")
    print(f"✅ Saved to: {output_path}")
    
    print(f"\n📊 Final Dataset Columns:")
    for col in final_df.columns:
        print(f"   • {col}")
    
    print(f"\n📈 Label Distribution:")
    label_counts = final_df['label'].value_counts()
    print(f"   Recommended (1): {label_counts.get(1, 0)} samples")
    print(f"   Not Recommended (0): {label_counts.get(0, 0)} samples")
    
except Exception as e:
    print(f"❌ Error during merging: {e}")
    print("\n💡 Creating a simplified training dataset...")
    
    # Create a simple dataset if merging fails
    simple_data = {
        'age': np.random.randint(13, 20, 100),
        'monthly_allowance': np.random.randint(500, 5000, 100),
        'financial_literacy_score': np.random.uniform(1, 10, 100).round(1),
        'risk_appetite': np.random.choice(['Low', 'Medium', 'High'], 100),
        'sip_amount': np.random.randint(100, 2000, 100),
        'fund_category': np.random.choice(['Equity', 'Debt', 'Hybrid'], 100),
        'fund_risk_category': np.random.choice(['Low', 'Medium', 'High'], 100),
        'label': np.random.choice([0, 1], 100, p=[0.3, 0.7])
    }
    
    simple_df = pd.DataFrame(simple_data)
    simple_df.to_csv('data/processed/final_sip_training_dataset.csv', index=False)
    print(f"✅ Created simple training dataset with {len(simple_df)} samples")