import json
import hashlib
import os

users = {
    "teen1": {
        "user_id": "000001",
        "password": hashlib.sha256("password123".encode()).hexdigest(),
        "email": "teen1@example.com",
        "age": 16,
        "created_at": "2024-01-01T10:00:00",
        "streak": 7,
        "total_invested": 15000,
        "portfolio_value": 16250,
        "achievements": ["7_day_streak", "first_investment"],
        "avatar_color": "#667eea",
        "nominee": {
            "name": "John Parent",
            "relationship": "Parent",
            "phone": "9876543210",
            "email": "parent@example.com",
            "id_proof": "Aadhaar Card",
            "id_number": "XXXX-XXXX-XXXX",
            "added_date": "2024-01-05T14:30:00"
        }
    },
    "investor": {
        "user_id": "000002",
        "password": hashlib.sha256("invest123".encode()).hexdigest(),
        "email": "investor@example.com",
        "age": 18,
        "created_at": "2024-01-15T09:00:00",
        "streak": 15,
        "total_invested": 35000,
        "portfolio_value": 37800,
        "achievements": ["7_day_streak", "first_investment", "thousand_points"],
        "avatar_color": "#10b981"
    }
}

os.makedirs("users", exist_ok=True)
os.makedirs("users/avatars", exist_ok=True)

with open("users/user_data.json", "w") as f:
    json.dump(users, f, indent=2)

print("✅ Sample users created!")
print("Username: teen1 | Password: password123")
print("Username: investor | Password: invest123")
