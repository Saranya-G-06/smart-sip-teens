import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import hashlib
import time
import random
from PIL import Image
import io
import base64
from pathlib import Path
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ModuleNotFoundError:
    install("plotly")
    import plotly.express as px
    import plotly.graph_objects as go


# Page Configuration
st.set_page_config(
    page_title="FinStride - Teen Financial App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Glass Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Streak Animation */
    .streak-badge {
        background: linear-gradient(45deg, #FF512F, #F09819);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: bold;
        animation: pulse 2s infinite;
        display: inline-block;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Profile Avatar */
    .profile-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(45deg, #667eea, #764ba2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin: 0 auto;
    }
    
    /* Achievement Badges */
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.2rem;
    }
    
    .badge-gold { background: linear-gradient(45deg, #FFD700, #FFA500); color: #333; }
    .badge-silver { background: linear-gradient(45deg, #C0C0C0, #A9A9A9); color: #333; }
    .badge-bronze { background: linear-gradient(45deg, #CD7F32, #8B4513); color: white; }
    
    /* Notification Bell */
    .notification-bell {
        position: relative;
        display: inline-block;
    }
    
    .notification-dot {
        position: absolute;
        top: -5px;
        right: -5px;
        width: 15px;
        height: 15px;
        background: #FF4757;
        border-radius: 50%;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# ========== AUTHENTICATION SYSTEM ==========
class AuthSystem:
    def __init__(self):
        self.users_file = "users/user_data.json"
        self.ensure_directories()
        self.load_users()
    
    def ensure_directories(self):
        os.makedirs("users", exist_ok=True)
        os.makedirs("users/avatars", exist_ok=True)
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password, email, age):
        if username in self.users:
            return False, "Username already exists!"
        
        user_id = str(len(self.users) + 1).zfill(6)
        self.users[username] = {
            "user_id": user_id,
            "password": self.hash_password(password),
            "email": email,
            "age": age,
            "created_at": datetime.now().isoformat(),
            "streak": 0,
            "total_invested": 0,
            "portfolio_value": 0,
            "achievements": [],
            "notifications": [],
            "nominee": None,
            "avatar_color": f"#{random.randint(0, 0xFFFFFF):06x}"
        }
        
        self.save_users()
        
        # Create user portfolio
        portfolio_file = f"users/{user_id}_portfolio.json"
        if not os.path.exists(portfolio_file):
            with open(portfolio_file, 'w') as f:
                json.dump({
                    "investments": [],
                    "transactions": [],
                    "goals": [],
                    "watchlist": []
                }, f)
        
        return True, f"Account created! Your ID: {user_id}"
    
    def login(self, username, password):
        if username not in self.users:
            return False, "User not found!"
        
        if self.users[username]["password"] == self.hash_password(password):
            return True, "Login successful!"
        else:
            return False, "Incorrect password!"
    
    def get_user_data(self, username):
        return self.users.get(username, {})

# ========== STREAK & GAMIFICATION SYSTEM ==========
class GamificationSystem:
    def __init__(self, username):
        self.username = username
        self.streak_file = f"users/{username}_streak.json"
        self.load_streak_data()
    
    def load_streak_data(self):
        if os.path.exists(self.streak_file):
            with open(self.streak_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "current_streak": 0,
                "longest_streak": 0,
                "last_login": None,
                "daily_checkins": [],
                "points": 100,
                "achievements": [],
                "badges": []
            }
    
    def save_streak_data(self):
        with open(self.streak_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def check_in(self):
        today = datetime.now().date().isoformat()
        
        if today not in self.data["daily_checkins"]:
            # Check if yesterday was checked in (for streak)
            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
            
            if self.data["last_login"] == yesterday:
                self.data["current_streak"] += 1
            elif self.data["last_login"] != today:
                self.data["current_streak"] = 1
            
            if self.data["current_streak"] > self.data["longest_streak"]:
                self.data["longest_streak"] = self.data["current_streak"]
            
            self.data["daily_checkins"].append(today)
            self.data["last_login"] = today
            
            # Add points
            self.data["points"] += 10 + (self.data["current_streak"] * 5)
            
            # Check for streak achievements
            self.check_achievements()
            
            self.save_streak_data()
            return True, f"🎉 Daily check-in complete! +{10 + (self.data['current_streak'] * 5)} points"
        else:
            return False, "Already checked in today!"
    
    def check_achievements(self):
        achievements = []
        
        if self.data["current_streak"] >= 7 and "7_day_streak" not in self.data["achievements"]:
            achievements.append({"id": "7_day_streak", "name": "Weekly Warrior", "points": 50})
            self.data["achievements"].append("7_day_streak")
        
        if self.data["current_streak"] >= 30 and "30_day_streak" not in self.data["achievements"]:
            achievements.append({"id": "30_day_streak", "name": "Monthly Master", "points": 200})
            self.data["achievements"].append("30_day_streak")
        
        if self.data["points"] >= 1000 and "thousand_points" not in self.data["achievements"]:
            achievements.append({"id": "thousand_points", "name": "Point Pioneer", "points": 100})
            self.data["achievements"].append("thousand_points")
        
        for ach in achievements:
            self.data["points"] += ach["points"]
        
        return achievements

# ========== INVESTMENT TRACKING SYSTEM ==========
class InvestmentTracker:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id
        self.portfolio_file = f"users/{user_id}_portfolio.json"
        self.load_portfolio()
    
    def load_portfolio(self):
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, 'r') as f:
                self.portfolio = json.load(f)
        else:
            self.portfolio = {
                "investments": [],
                "transactions": [],
                "goals": [
                    {"id": 1, "name": "College Fund", "target": 50000, "current": 0, "color": "#667eea"},
                    {"id": 2, "name": "Gaming PC", "target": 80000, "current": 0, "color": "#764ba2"},
                    {"id": 3, "name": "Trip with Friends", "target": 30000, "current": 0, "color": "#10b981"}
                ],
                "watchlist": []
            }
    
    def save_portfolio(self):
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f, indent=2)
    
    def add_investment(self, fund_name, amount, fund_type, risk_level):
        investment_id = len(self.portfolio["investments"]) + 1
        
        investment = {
            "id": investment_id,
            "fund_name": fund_name,
            "amount": amount,
            "fund_type": fund_type,
            "risk_level": risk_level,
            "date": datetime.now().isoformat(),
            "current_value": amount * random.uniform(0.95, 1.05),  # Simulated growth
            "returns": 0
        }
        
        self.portfolio["investments"].append(investment)
        
        # Add transaction
        transaction = {
            "id": len(self.portfolio["transactions"]) + 1,
            "type": "INVESTMENT",
            "amount": amount,
            "description": f"Invested in {fund_name}",
            "date": datetime.now().isoformat(),
            "status": "COMPLETED"
        }
        
        self.portfolio["transactions"].append(transaction)
        
        # Update goals
        for goal in self.portfolio["goals"]:
            goal["current"] += amount * 0.3  # Distribute investment across goals
        
        self.save_portfolio()
        return investment
    
    def get_portfolio_summary(self):
        total_invested = sum(inv["amount"] for inv in self.portfolio["investments"])
        current_value = sum(inv.get("current_value", inv["amount"]) for inv in self.portfolio["investments"])
        total_returns = current_value - total_invested
        returns_percentage = (total_returns / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "total_invested": total_invested,
            "current_value": current_value,
            "total_returns": total_returns,
            "returns_percentage": returns_percentage,
            "investment_count": len(self.portfolio["investments"])
        }

# ========== INITIALIZE SESSION STATE ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.current_page = "login"
    st.session_state.auth = AuthSystem()

# ========== LOGIN/SIGNUP PAGE ==========
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #667eea; font-size: 3rem;">💰 FinStride</h1>
            <p style="color: #666; font-size: 1.2rem;">Your Teen Financial Companion</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.subheader("Welcome Back!")
            
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("🚀 Login", use_container_width=True):
                success, message = st.session_state.auth.login(login_username, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.user_data = st.session_state.auth.get_user_data(login_username)
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                else:
                    st.error(message)
        
        with tab2:
            st.subheader("Start Your Financial Journey!")
            
            reg_username = st.text_input("Choose Username", key="reg_user")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_age = st.number_input("Age", 13, 19, 16, key="reg_age")
            reg_password = st.text_input("Create Password", type="password", key="reg_pass")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("🎯 Create Account", use_container_width=True):
                if reg_password != reg_confirm:
                    st.error("Passwords don't match!")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters!")
                else:
                    success, message = st.session_state.auth.register(
                        reg_username, reg_password, reg_email, reg_age
                    )
                    if success:
                        st.success(message)
                        st.info("Please login with your new account")
                    else:
                        st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== DASHBOARD PAGE ==========
def dashboard_page():
    # Initialize systems
    gamification = GamificationSystem(st.session_state.username)
    tracker = InvestmentTracker(
        st.session_state.username,
        st.session_state.user_data["user_id"]
    )
    
    # Auto check-in
    if "checked_in_today" not in st.session_state:
        success, message = gamification.check_in()
        if success:
            st.toast(message, icon="🎉")
        st.session_state.checked_in_today = True
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div class="profile-avatar">
                {st.session_state.username[0].upper()}
            </div>
            <h3 style="margin: 0.5rem 0;">@{st.session_state.username}</h3>
            <p style="color: #666; margin: 0;">ID: {st.session_state.user_data['user_id']}</p>
            <div class="streak-badge" style="margin: 1rem 0;">
                🔥 {gamification.data['current_streak']} Day Streak
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "💰 Invest Now", "📈 Portfolio", "🎮 Gamification", 
             "👥 Nominee", "🎯 Goals", "⚙️ Profile"],
            label_visibility="collapsed"
        )
        
        st.session_state.current_page = page.split(" ")[1].lower()
        
        st.markdown("---")
        
        # Quick Stats
        portfolio_summary = tracker.get_portfolio_summary()
        
        st.metric("💰 Portfolio Value", f"₹{portfolio_summary['current_value']:,.0f}")
        st.metric("🎯 Points", f"{gamification.data['points']:,}")
        st.metric("📊 Returns", f"{portfolio_summary['returns_percentage']:.1f}%")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "login"
            st.rerun()
    
    # Main Content based on selected page
    if st.session_state.current_page == "dashboard":
        show_main_dashboard(gamification, tracker, portfolio_summary)
    elif st.session_state.current_page == "invest":
        show_investment_page(tracker)
    elif st.session_state.current_page == "portfolio":
        show_portfolio_page(tracker)
    elif st.session_state.current_page == "gamification":
        show_gamification_page(gamification)
    elif st.session_state.current_page == "nominee":
        show_nominee_page()
    elif st.session_state.current_page == "goals":
        show_goals_page(tracker)
    elif st.session_state.current_page == "profile":
        show_profile_page()

# ========== MAIN DASHBOARD ==========
def show_main_dashboard(gamification, tracker, portfolio_summary):
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">Welcome back, {st.session_state.username}! 👋</h1>
        <div style="display: flex; gap: 1rem;">
            <span class="badge badge-gold">🌟 {len(gamification.data['achievements'])} Achievements</span>
            <span class="notification-bell">
                🔔 <span class="notification-dot"></span>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"*Last login: {datetime.now().strftime('%I:%M %p')}*")
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("🔥 Current Streak", gamification.data['current_streak'], 
                 f"Longest: {gamification.data['longest_streak']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("💰 Total Invested", f"₹{portfolio_summary['total_invested']:,.0f}",
                 f"{portfolio_summary['investment_count']} investments")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("📈 Portfolio Value", f"₹{portfolio_summary['current_value']:,.0f}",
                 f"{portfolio_summary['returns_percentage']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("🎯 Points", f"{gamification.data['points']:,}", "+100 today")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Investment Chart
    st.markdown("### 📊 Investment Growth")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create sample growth data
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        values = [1000 + i*500 + random.randint(-200, 200) for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=values,
            mode='lines+markers',
            name='Portfolio',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎮 Quick Actions")
        
        if st.button("💰 Add Investment", use_container_width=True):
            st.session_state.current_page = "invest"
            st.rerun()
        
        if st.button("🎯 Set Goal", use_container_width=True):
            st.session_state.current_page = "goals"
            st.rerun()
        
        if st.button("👥 Add Nominee", use_container_width=True):
            st.session_state.current_page = "nominee"
            st.rerun()
        
        if st.button("🔥 Streak Info", use_container_width=True):
            st.session_state.current_page = "gamification"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity & Goals
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Recent Activity")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        activities = [
            {"time": "2 min ago", "action": "Daily check-in", "points": "+15"},
            {"time": "1 hour ago", "action": "Added ₹1,000 to College Fund", "points": "+10"},
            {"time": "3 hours ago", "action": "Completed Financial Quiz", "points": "+25"},
            {"time": "Yesterday", "action": "7-day streak achieved", "points": "+50"},
            {"time": "2 days ago", "action": "Started SIP in Equity Fund", "points": "+30"},
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div style="padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: bold;">{activity['action']}</span>
                    <span style="color: #10b981;">{activity['points']}</span>
                </div>
                <small style="color: #888;">{activity['time']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Financial Goals")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        for goal in tracker.portfolio["goals"][:3]:
            progress = (goal["current"] / goal["target"]) * 100
            st.markdown(f"**{goal['name']}**")
            st.progress(min(progress / 100, 1.0))
            st.caption(f"₹{goal['current']:,.0f} / ₹{goal['target']:,.0f} ({progress:.1f}%)")
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== INVESTMENT PAGE ==========
def show_investment_page(tracker):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 💰 Smart Investment Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📈 SIP Recommender", "💼 Invest Now", "📊 Fund Explorer"])
    
    with tab1:
        st.markdown("### 🤖 AI-Powered SIP Recommendation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", 13, 19, st.session_state.user_data.get("age", 16))
            monthly_allowance = st.number_input("Monthly Allowance (₹)", 500, 50000, 3000)
            financial_literacy = st.slider("Financial Literacy (1-10)", 1, 10, 6)
        
        with col2:
            risk_appetite = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])
            saving_habit = st.selectbox("Saving Habit", ["Saver", "Balanced", "Spender"])
            investment_goal = st.selectbox("Primary Goal", ["Education", "Gadget", "Travel", "Wealth"])
        
        st.markdown("### 💡 Fund Suggestions")
        
        funds = [
            {"name": "Teen Starter Fund", "type": "Hybrid", "risk": "Low", "min_sip": 500, "returns": "10-12%"},
            {"name": "Future Scholar Fund", "type": "Equity", "risk": "Medium", "min_sip": 1000, "returns": "12-15%"},
            {"name": "Growth Accelerator", "type": "Equity", "risk": "High", "min_sip": 2000, "returns": "15-18%"},
            {"name": "Safe Saver Fund", "type": "Debt", "risk": "Low", "min_sip": 500, "returns": "7-9%"},
        ]
        
        for fund in funds:
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{fund['name']}**")
                st.caption(f"{fund['type']} • {fund['risk']} Risk")
            with col2:
                st.markdown(f"**Min SIP:** ₹{fund['min_sip']}")
            with col3:
                if st.button(f"Invest", key=f"invest_{fund['name']}"):
                    st.success(f"Added {fund['name']} to your portfolio!")
    
    with tab2:
        st.markdown("### 💼 Quick Investment")
        
        fund_name = st.selectbox("Select Fund", [f["name"] for f in funds])
        amount = st.number_input("Investment Amount (₹)", 500, 50000, 1000, step=500)
        duration = st.selectbox("Duration", ["6 months", "1 year", "3 years", "5 years"])
        
        if st.button("🚀 Confirm Investment", use_container_width=True):
            selected_fund = next(f for f in funds if f["name"] == fund_name)
            investment = tracker.add_investment(
                fund_name, amount, selected_fund["type"], selected_fund["risk"]
            )
            
            st.success(f"✅ Investment of ₹{amount} in {fund_name} successful!")
            st.balloons()
            
            # Show investment details
            st.markdown("### 📋 Investment Details")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Investment ID", investment["id"])
                st.metric("Amount", f"₹{investment['amount']:,}")
            with col2:
                st.metric("Date", datetime.now().strftime("%d %b %Y"))
                st.metric("Estimated Value", f"₹{investment['current_value']:,.0f}")
    
    with tab3:
        st.markdown("### 📊 Fund Performance Explorer")
        
        # Create sample fund performance data
        fund_data = pd.DataFrame({
            'Fund': ['Teen Starter', 'Future Scholar', 'Growth Accelerator', 'Safe Saver'],
            '1 Month': [2.5, 3.2, 4.1, 1.8],
            '3 Months': [7.2, 9.5, 12.3, 5.4],
            '6 Months': [14.5, 18.2, 24.7, 10.8],
            '1 Year': [28.4, 35.6, 42.3, 19.7]
        })
        
        st.dataframe(fund_data.style.highlight_max(axis=0), use_container_width=True)
        
        # Performance chart
        fig = px.bar(fund_data, x='Fund', y=['1 Month', '3 Months', '6 Months', '1 Year'],
                    title="Fund Returns Comparison", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== PORTFOLIO PAGE ==========
def show_portfolio_page(tracker):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📈 Your Investment Portfolio")
    
    portfolio_summary = tracker.get_portfolio_summary()
    
    # Portfolio Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Invested", f"₹{portfolio_summary['total_invested']:,.0f}")
    with col2:
        st.metric("Current Value", f"₹{portfolio_summary['current_value']:,.0f}")
    with col3:
        st.metric("Total Returns", f"₹{portfolio_summary['total_returns']:,.0f}")
    with col4:
        st.metric("Returns %", f"{portfolio_summary['returns_percentage']:.1f}%")
    
    # Investments Table
    st.markdown("### 📋 Your Investments")
    
    if tracker.portfolio["investments"]:
        investments_df = pd.DataFrame(tracker.portfolio["investments"])
        st.dataframe(investments_df, use_container_width=True)
        
        # Allocation Chart
        if len(investments_df) > 0:
            fig = px.pie(investments_df, values='amount', names='fund_name',
                        title="Portfolio Allocation", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No investments yet. Start investing to build your portfolio!")
    
    # Transaction History
    st.markdown("### 📝 Transaction History")
    
    if tracker.portfolio["transactions"]:
        transactions_df = pd.DataFrame(tracker.portfolio["transactions"])
        st.dataframe(transactions_df, use_container_width=True)
    else:
        st.info("No transactions yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== GAMIFICATION PAGE ==========
def show_gamification_page(gamification):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🎮 Gamification & Rewards")
    
    # Streak Information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔥 Current Streak", gamification.data["current_streak"])
    with col2:
        st.metric("🏆 Longest Streak", gamification.data["longest_streak"])
    with col3:
        st.metric("🎯 Total Points", gamification.data["points"])
    
    # Streak Calendar
    st.markdown("### 📅 Streak Calendar")
    
    # Create calendar view
    today = datetime.now().date()
    month_days = []
    
    for i in range(30):
        day = today - timedelta(days=29-i)
        month_days.append(day)
    
    # Display calendar
    cols = st.columns(7)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    for i, day_name in enumerate(day_names):
        cols[i].markdown(f"**{day_name}**")
    
    for i, day in enumerate(month_days):
        col_idx = i % 7
        day_str = day.isoformat()
        
        if day_str in gamification.data["daily_checkins"]:
            cols[col_idx].markdown(f"<div style='background: #10b981; color: white; padding: 5px; border-radius: 5px; text-align: center;'>✓</div>", unsafe_allow_html=True)
        else:
            cols[col_idx].markdown(f"<div style='background: #eee; padding: 5px; border-radius: 5px; text-align: center;'>{day.day}</div>", unsafe_allow_html=True)
    
    # Achievements
    st.markdown("### 🏆 Achievements")
    
    achievements = [
        {"id": "7_day_streak", "name": "Weekly Warrior", "desc": "Maintain 7-day streak", "points": 50, "icon": "🔥"},
        {"id": "30_day_streak", "name": "Monthly Master", "desc": "Maintain 30-day streak", "points": 200, "icon": "👑"},
        {"id": "first_investment", "name": "First Step", "desc": "Make your first investment", "points": 100, "icon": "💰"},
        {"id": "thousand_points", "name": "Point Pioneer", "desc": "Reach 1000 points", "points": 100, "icon": "🎯"},
        {"id": "goal_achiever", "name": "Goal Getter", "desc": "Complete a financial goal", "points": 150, "icon": "🏆"},
        {"id": "portfolio_diversifier", "name": "Diversifier", "desc": "Invest in 3 different funds", "points": 75, "icon": "📊"},
    ]
    
    cols = st.columns(3)
    
    for idx, achievement in enumerate(achievements):
        with cols[idx % 3]:
            unlocked = achievement["id"] in gamification.data["achievements"]
            
            if unlocked:
                st.markdown(f"""
                <div style="background: linear-gradient(45deg, #FFD700, #FFA500); padding: 1rem; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2rem;">{achievement['icon']}</div>
                    <h4>{achievement['name']}</h4>
                    <p>{achievement['desc']}</p>
                    <small>+{achievement['points']} points</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #eee; padding: 1rem; border-radius: 10px; text-align: center; opacity: 0.5;">
                    <div style="font-size: 2rem;">{achievement['icon']}</div>
                    <h4>{achievement['name']}</h4>
                    <p>{achievement['desc']}</p>
                    <small>Locked</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Daily Challenge
    st.markdown("### 🎯 Daily Challenge")
    
    challenges = [
        {"name": "Financial Quiz", "points": 25, "completed": False},
        {"name": "Watch Educational Video", "points": 15, "completed": True},
        {"name": "Check Portfolio", "points": 10, "completed": False},
        {"name": "Set Savings Goal", "points": 20, "completed": True},
    ]
    
    for challenge in challenges:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{challenge['name']}**")
        with col2:
            st.markdown(f"+{challenge['points']} pts")
        with col3:
            if challenge['completed']:
                st.success("✅ Done")
            else:
                if st.button("Start", key=f"challenge_{challenge['name']}"):
                    st.success(f"Started {challenge['name']}!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== NOMINEE PAGE ==========
def show_nominee_page():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 👥 Nominee Management")
    
    st.markdown("""
    ### Why Add a Nominee?
    A nominee ensures your investments are transferred to your chosen person 
    (usually parent/guardian) in case of any unforeseen circumstances.
    
    **For teens under 18, this is mandatory.**
    """)
    
    tab1, tab2 = st.tabs(["➕ Add Nominee", "👀 View Nominee"])
    
    with tab1:
        st.markdown("### Add Nominee Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nominee_name = st.text_input("Nominee Name")
            relationship = st.selectbox("Relationship", 
                                      ["Parent", "Guardian", "Sibling", "Other"])
            phone = st.text_input("Phone Number")
        
        with col2:
            email = st.text_input("Email Address")
            id_proof = st.selectbox("ID Proof Type", 
                                   ["Aadhaar Card", "PAN Card", "Passport", "Driving License"])
            id_number = st.text_input("ID Proof Number")
        
        if st.button("✅ Save Nominee", use_container_width=True):
            # Save nominee data
            nominee_data = {
                "name": nominee_name,
                "relationship": relationship,
                "phone": phone,
                "email": email,
                "id_proof": id_proof,
                "id_number": id_number,
                "added_date": datetime.now().isoformat()
            }
            
            # Update user data
            st.session_state.user_data["nominee"] = nominee_data
            st.session_state.auth.users[st.session_state.username]["nominee"] = nominee_data
            st.session_state.auth.save_users()
            
            st.success("✅ Nominee added successfully!")
            st.balloons()
    
    with tab2:
        if st.session_state.user_data.get("nominee"):
            nominee = st.session_state.user_data["nominee"]
            
            st.markdown("### Current Nominee")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Name", nominee["name"])
                st.metric("Relationship", nominee["relationship"])
                st.metric("Phone", nominee["phone"])
            
            with col2:
                st.metric("Email", nominee["email"])
                st.metric("ID Proof", nominee["id_proof"])
                st.metric("Added On", datetime.fromisoformat(nominee["added_date"]).strftime("%d %b %Y"))
            
            # Nominee certificate
            st.markdown("### 📜 Nominee Certificate")
            st.markdown("""
            <div style="border: 2px solid #667eea; padding: 2rem; border-radius: 10px; background: white;">
                <h3 style="text-align: center; color: #667eea;">NOMINEE CERTIFICATE</h3>
                <p>This certifies that <strong>{nominee_name}</strong> is the nominated beneficiary 
                for all investments made by <strong>{username}</strong> on the FinStride platform.</p>
                <br>
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>User Signature:</strong><br>
                        <em>{username}</em>
                    </div>
                    <div>
                        <strong>Date:</strong><br>
                        {date}
                    </div>
                </div>
            </div>
            """.format(
                nominee_name=nominee["name"],
                username=st.session_state.username,
                date=datetime.now().strftime("%d %B, %Y")
            ), unsafe_allow_html=True)
            
            if st.button("📄 Download Certificate", use_container_width=True):
                st.success("Certificate downloaded (demo feature)")
        else:
            st.info("No nominee added yet. Please add a nominee above.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== GOALS PAGE ==========
def show_goals_page(tracker):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🎯 Financial Goals")
    
    tab1, tab2 = st.tabs(["🎯 My Goals", "➕ Set New Goal"])
    
    with tab1:
        if tracker.portfolio["goals"]:
            for goal in tracker.portfolio["goals"]:
                progress = (goal["current"] / goal["target"]) * 100
                
                st.markdown(f"### {goal['name']}")
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.progress(min(progress / 100, 1.0))
                    st.caption(f"₹{goal['current']:,.0f} / ₹{goal['target']:,.0f} ({progress:.1f}%)")
                
                with col2:
                    days_left = (goal["target"] - goal["current"]) / 1000 * 30
                    st.metric("Est. Days", f"{int(days_left)}")
                
                with col3:
                    if st.button("Add ₹", key=f"add_{goal['id']}"):
                        amount = st.number_input("Amount", 100, 10000, 1000)
                        goal["current"] += amount
                        tracker.save_portfolio()
                        st.success(f"Added ₹{amount} to {goal['name']}")
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No goals set yet. Create your first goal!")
    
    with tab2:
        st.markdown("### Create New Goal")
        
        goal_name = st.text_input("Goal Name (e.g., 'New Laptop', 'College Fund')")
        target_amount = st.number_input("Target Amount (₹)", 1000, 1000000, 50000)
        timeline = st.selectbox("Target Timeline", 
                              ["3 months", "6 months", "1 year", "2 years", "5 years"])
        priority = st.select_slider("Priority", ["Low", "Medium", "High"])
        
        if st.button("🎯 Create Goal", use_container_width=True):
            new_goal = {
                "id": len(tracker.portfolio["goals"]) + 1,
                "name": goal_name,
                "target": target_amount,
                "current": 0,
                "timeline": timeline,
                "priority": priority,
                "color": f"#{random.randint(0, 0xFFFFFF):06x}",
                "created": datetime.now().isoformat()
            }
            
            tracker.portfolio["goals"].append(new_goal)
            tracker.save_portfolio()
            
            st.success(f"Goal '{goal_name}' created successfully!")
            st.balloons()
    
    # Goal visualization
    st.markdown("### 📊 Goals Progress")
    
    if tracker.portfolio["goals"]:
        goals_df = pd.DataFrame(tracker.portfolio["goals"])
        
        fig = px.bar(goals_df, x='name', y=['current', 'target'], 
                    barmode='group', title="Goals Progress",
                    labels={'value': 'Amount (₹)', 'variable': 'Type'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== PROFILE PAGE ==========
def show_profile_page():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Profile Settings")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="profile-avatar" style="background: {st.session_state.user_data.get('avatar_color', '#667eea')};">
                {st.session_state.username[0].upper()}
            </div>
            <h3>@{st.session_state.username}</h3>
            <p style="color: #666;">User ID: {st.session_state.user_data['user_id']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Personal Information")
        
        user_data = st.session_state.user_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Username", value=st.session_state.username, disabled=True)
            st.text_input("Email", value=user_data.get("email", ""))
        
        with col2:
            st.number_input("Age", value=user_data.get("age", 16), min_value=13, max_value=19)
            st.text_input("Account Created", 
                         value=datetime.fromisoformat(user_data.get("created_at", datetime.now().isoformat())).strftime("%d %b %Y"),
                         disabled=True)
    
    # Security Settings
    st.markdown("### 🔒 Security")
    
    tab1, tab2, tab3 = st.tabs(["Change Password", "Privacy", "Notifications"])
    
    with tab1:
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Password", use_container_width=True):
            if new_pass == confirm_pass:
                st.success("Password updated successfully!")
            else:
                st.error("Passwords don't match!")
    
    with tab2:
        st.checkbox("Show portfolio value publicly", value=False)
        st.checkbox("Allow friend requests", value=True)
        st.checkbox("Share achievements", value=True)
        st.checkbox("Email notifications", value=True)
        
        if st.button("Save Privacy Settings", use_container_width=True):
            st.success("Privacy settings saved!")
    
    with tab3:
        st.markdown("### 🔔 Notification Preferences")
        
        notifications = [
            {"name": "Investment Updates", "desc": "Get notified about portfolio changes", "enabled": True},
            {"name": "Goal Reminders", "desc": "Reminders about your financial goals", "enabled": True},
            {"name": "Streak Alerts", "desc": "Don't break your streak!", "enabled": True},
            {"name": "Market News", "desc": "Weekly financial news digest", "enabled": False},
            {"name": "Educational Content", "desc": "Financial tips and articles", "enabled": True},
        ]
        
        for notif in notifications:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{notif['name']}**")
                st.caption(notif['desc'])
            with col2:
                st.checkbox("", value=notif['enabled'], key=f"notif_{notif['name']}")
    
    # Account Statistics
    st.markdown("### 📊 Account Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days_active = (datetime.now() - datetime.fromisoformat(user_data["created_at"])).days
        st.metric("Days Active", days_active)
    
    with col2:
        st.metric("Total Logins", "∞")  # Would be tracked in real app
    
    with col3:
        st.metric("Friends", "0")  # Social feature placeholder
    
    with col4:
        st.metric("App Version", "2.0.1")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== MAIN APP FLOW ==========
def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()