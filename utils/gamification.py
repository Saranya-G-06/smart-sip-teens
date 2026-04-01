import json
import sqlite3
from utils.database import get_connection

BADGES = {
    "Beginner Investor": {"icon": "🌱", "desc": "Earned 50+ points", "threshold": 50},
    "SIP Starter": {"icon": "💰", "desc": "Earned 200+ points", "threshold": 200},
    "Investment Pro": {"icon": "🏆", "desc": "Earned 500+ points", "threshold": 500},
    "Streak Master": {"icon": "🔥", "desc": "7+ day streak", "threshold": 700},
}

def get_gamification(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT total_points, lessons_completed, badges FROM gamification WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"points": row[0], "lessons": json.loads(row[1]), "badges": json.loads(row[2])}
    return {"points": 0, "lessons": [], "badges": []}

def add_points(user_id, points, reason=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE gamification SET total_points = total_points + ? WHERE user_id=?", (points, user_id))
    conn.commit()
    conn.close()
    check_badges(user_id)

def complete_lesson(user_id, lesson_title, points):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT lessons_completed, total_points FROM gamification WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        lessons = json.loads(row[0])
        if lesson_title not in lessons:
            lessons.append(lesson_title)
            c.execute("UPDATE gamification SET lessons_completed=?, total_points=total_points+? WHERE user_id=?",
                      (json.dumps(lessons), points, user_id))
            conn.commit()
            conn.close()
            check_badges(user_id)
            return True, points
    conn.close()
    return False, 0

def check_badges(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT total_points, badges FROM gamification WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return
    points, badges_json = row
    badges = json.loads(badges_json)
    for badge, info in BADGES.items():
        if points >= info["threshold"] and badge not in badges:
            badges.append(badge)
    c.execute("UPDATE gamification SET badges=? WHERE user_id=?", (json.dumps(badges), user_id))
    conn.commit()
    conn.close()
