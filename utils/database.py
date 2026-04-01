import sqlite3
import os

DB_PATH = "database/users.db"

def get_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS streaks (
        user_id INTEGER PRIMARY KEY,
        current_streak INTEGER DEFAULT 0,
        highest_streak INTEGER DEFAULT 0,
        last_login DATE,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        monthly_allowance REAL,
        savings_rate REAL,
        risk_tolerance TEXT,
        investment_goal TEXT,
        investment_horizon INTEGER,
        financial_literacy_score INTEGER DEFAULT 50,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS gamification (
        user_id INTEGER PRIMARY KEY,
        total_points INTEGER DEFAULT 0,
        lessons_completed TEXT DEFAULT '[]',
        badges TEXT DEFAULT '[]',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()
