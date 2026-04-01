import pandas as pd
import numpy as np

np.random.seed(42)
n = 3000

ages = np.random.randint(13, 20, n)
allowances = np.random.randint(500, 5000, n)
savings_rates = np.random.uniform(0.05, 0.60, n)
literacy_scores = np.random.randint(30, 100, n)
horizons = np.random.randint(1, 15, n)
risk_tolerances = np.random.choice(['Low', 'Medium', 'High'], n)

# SIP recommendation formula
risk_factor = np.where(np.array(risk_tolerances) == 'High', 1.3,
              np.where(np.array(risk_tolerances) == 'Medium', 1.1, 0.9))
recommended_sip = (allowances * savings_rates * (0.5 + 0.02*literacy_scores/100 + 0.03*horizons/15) * risk_factor).astype(int)
recommended_sip = np.clip(recommended_sip, 100, 3000)

teen_df = pd.DataFrame({
    'age': ages,
    'monthly_allowance': allowances,
    'savings_rate': np.round(savings_rates, 2),
    'financial_literacy_score': literacy_scores,
    'investment_horizon': horizons,
    'risk_tolerance': risk_tolerances,
    'recommended_sip': recommended_sip
})
teen_df.to_csv('/home/claude/SmartSIP_Teens/data/teen_finance_dataset.csv', index=False)

# Mutual funds
fund_names = [f"Fund {chr(65+i%26)}{i//26 if i>=26 else ''}" for i in range(60)]
categories = np.random.choice(['Equity', 'Debt', 'Hybrid', 'ELSS', 'Index'], 60)
risk_levels = np.random.choice(['Low', 'Medium', 'High'], 60)
returns_1y = np.round(np.random.uniform(4, 25, 60), 2)
returns_3y = np.round(np.random.uniform(6, 20, 60), 2)
returns_5y = np.round(np.random.uniform(8, 18, 60), 2)
min_sip = np.random.choice([100, 200, 500, 1000], 60)

funds_df = pd.DataFrame({
    'fund_name': fund_names,
    'category': categories,
    'risk_level': risk_levels,
    '1y_return': returns_1y,
    '3y_return': returns_3y,
    '5y_return': returns_5y,
    'min_sip': min_sip
})
funds_df.to_csv('/home/claude/SmartSIP_Teens/data/mutual_funds.csv', index=False)

# Financial lessons
lessons = [
    ("What is SIP?", "SIP (Systematic Investment Plan) is a method of investing a fixed sum regularly in mutual funds.", "Beginner", 10),
    ("Power of Compounding", "Compounding means earning returns on your returns. The earlier you start, the more you earn!", "Beginner", 15),
    ("Risk vs Return", "Higher potential returns usually come with higher risk. Balancing both is key to smart investing.", "Intermediate", 20),
    ("Diversification", "Don't put all eggs in one basket. Spread investments across assets to reduce risk.", "Intermediate", 20),
    ("Inflation Basics", "Inflation erodes money's value over time. Investing helps your money grow faster than inflation.", "Beginner", 10),
    ("Mutual Funds 101", "Mutual funds pool money from many investors to buy a diversified portfolio of assets.", "Beginner", 15),
    ("Stock Market Basics", "Stock markets allow companies to raise capital and investors to own a piece of companies.", "Intermediate", 25),
    ("Goal-Based Investing", "Set clear financial goals and invest accordingly — short, medium, or long term.", "Intermediate", 20),
    ("Tax Benefits of ELSS", "ELSS funds offer tax deduction under Section 80C while providing equity market exposure.", "Advanced", 30),
    ("Reading Fund Factsheets", "Fund factsheets contain crucial data: NAV, AUM, portfolio composition, and past performance.", "Advanced", 35),
]
lessons_df = pd.DataFrame(lessons, columns=['title', 'description', 'level', 'reward_points'])
lessons_df.to_csv('/home/claude/SmartSIP_Teens/data/financial_lessons.csv', index=False)

# Sample users
sample_users = pd.DataFrame({
    'username': [f'teen{i}' for i in range(1, 21)],
    'age': np.random.randint(13, 20, 20),
    'monthly_allowance': np.random.randint(500, 5000, 20),
    'total_points': np.random.randint(0, 500, 20),
    'streak': np.random.randint(0, 30, 20),
})
sample_users.to_csv('/home/claude/SmartSIP_Teens/data/sample_users.csv', index=False)

print("All datasets created!")
