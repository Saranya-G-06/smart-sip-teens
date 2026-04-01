"""Setup demo user for testing."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.database import init_db, create_user, save_profile, add_points
import hashlib

def setup_demo():
    init_db()
    ph = hashlib.sha256("demo123".encode()).hexdigest()
    result = create_user("demo", "demo@smartsip.com", ph, 17)
    if result:
        from utils.database import get_user_by_username
        user = get_user_by_username("demo")
        if user:
            save_profile(user['id'], {
                'monthly_allowance': 2000,
                'savings_rate': 0.35,
                'risk_tolerance': 'Medium',
                'investment_goal': 'Wealth Building',
                'investment_horizon': 8,
                'financial_literacy_score': 65
            })
            add_points(user['id'], 45)
            print("✅ Demo user created: username=demo, password=demo123")
    else:
        print("ℹ️ Demo user already exists")

if __name__ == "__main__":
    setup_demo()
