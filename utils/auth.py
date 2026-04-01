import hashlib
import sqlite3
from datetime import date, datetime
from utils.database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username, email, password, age):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, password_hash, age) VALUES (?,?,?,?)",
                  (username, email, hash_password(password), age))
        conn.commit()
        user_id = c.lastrowid
        c.execute("INSERT INTO streaks (user_id, current_streak, highest_streak, last_login) VALUES (?,0,0,?)",
                  (user_id, str(date.today())))
        c.execute("INSERT INTO gamification (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists."
        return False, "Email already registered."
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, password_hash, age FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[1] == hash_password(password):
        return True, {"id": row[0], "username": username, "age": row[2]}
    return False, None

def update_streak(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT current_streak, highest_streak, last_login FROM streaks WHERE user_id=?", (user_id,))
    row = c.fetchone()
    today = date.today()
    if row:
        current, highest, last = row
        if last:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            delta = (today - last_date).days
            if delta == 1:
                current += 1
            elif delta > 1:
                current = 1
        else:
            current = 1
        highest = max(highest, current)
        c.execute("UPDATE streaks SET current_streak=?, highest_streak=?, last_login=? WHERE user_id=?",
                  (current, highest, str(today), user_id))
    else:
        c.execute("INSERT INTO streaks VALUES (?,1,1,?)", (user_id, str(today)))
    conn.commit()
    conn.close()
    return current, highest

def get_streak(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT current_streak, highest_streak FROM streaks WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row if row else (0, 0)
