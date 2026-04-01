import streamlit as st
from utils.database import get_gamification, get_streak
from utils.gamification import get_level, get_progress_pct, BADGES, POINT_ACTIONS

def render():
    user_id = st.session_state['user_id']
    user = st.session_state['user']
    gami = get_gamification(user_id)
    streak = get_streak(user_id)
    level = get_level(gami['total_points'])

    st.markdown("""
    <div style="background: linear-gradient(135deg, #bf360c, #e64a19); 
         padding: 20px; border-radius: 12px; margin-bottom: 24px;">
        <h2 style="color: #ffccbc; margin:0;">🏆 Gamification Center</h2>
        <p style="color: #ffccbc; margin:4px 0 0 0; opacity:0.8;">
            Earn points, unlock badges, and climb the ranks!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Level + XP
    points = gami['total_points']
    progress_pct = get_progress_pct(points)
    next_pts = level.get('next')

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 24px; border-radius: 16px; text-align:center">
            <div style="font-size: 4rem">{level['icon']}</div>
            <div style="color: #fff; font-size: 1.5rem; font-weight: 800; margin-top: 8px">{level['name']}</div>
            <div style="color: #90a4ae; font-size: 0.9rem">@{user['username']}</div>
            <div style="color: #ffd54f; font-size: 2rem; font-weight: 800; margin-top: 16px">⭐ {points}</div>
            <div style="color: #90a4ae; font-size: 0.8rem">Total Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Progress to Next Level")
        if next_pts:
            st.progress(progress_pct / 100, text=f"{progress_pct}% to next level ({next_pts - points} points needed)")
        else:
            st.progress(1.0, text="🏆 MAX LEVEL ACHIEVED!")
        
        st.markdown("#### 🔥 Streak Stats")
        s_col1, s_col2 = st.columns(2)
        s_col1.metric("Current Streak", f"{streak['current']} days", delta="🔥 Keep it up!")
        s_col2.metric("Best Streak", f"{streak['highest']} days")

        st.markdown("#### 📈 Activity Summary")
        act_col1, act_col2, act_col3 = st.columns(3)
        act_col1.metric("Lessons Done", len(gami['lessons_completed']))
        act_col2.metric("Simulator Uses", gami['simulator_uses'])
        act_col3.metric("Badges Earned", len(gami['badges']))

    # Badges section
    st.markdown("---")
    st.markdown("### 🎖️ Badge Collection")
    
    earned = gami.get('badges', [])
    badge_cols = st.columns(4)
    
    for i, (badge_name, badge_info) in enumerate(BADGES.items()):
        with badge_cols[i]:
            is_earned = badge_name in earned
            st.markdown(f"""
            <div style="padding:20px; border-radius:16px; text-align:center; margin-bottom:8px;
                        background: {'linear-gradient(135deg, rgba(0,230,118,0.15), rgba(0,150,80,0.1))' if is_earned else 'rgba(255,255,255,0.03)'};
                        border: 2px solid {'#00e676' if is_earned else '#333'};
                        {'box-shadow: 0 0 20px rgba(0,230,118,0.3);' if is_earned else ''}">
                <div style="font-size:3rem; {'filter: grayscale(0%)' if is_earned else 'filter: grayscale(100%); opacity:0.4'}">{badge_info['icon']}</div>
                <div style="color:{'#00e676' if is_earned else '#546e7a'}; font-weight:700; margin-top:8px">{badge_name}</div>
                <div style="color:#78909c; font-size:0.75rem; margin-top:4px">{badge_info['description']}</div>
                <div style="margin-top:8px; color:{'#00e676' if is_earned else '#546e7a'}; font-size:0.8rem">
                    {'✅ EARNED!' if is_earned else '🔒 Locked'}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # How to earn points
    st.markdown("---")
    st.markdown("### 💡 How to Earn Points")
    
    actions = [
        ("🔑 Daily Login", "+5 pts", "Log in every day to keep your streak alive"),
        ("📚 Complete a Lesson", "+10–35 pts", "Learn finance concepts in the Education Hub"),
        ("🧮 Use the Simulator", "+10 pts", "Run a SIP simulation to plan your investment"),
        ("👤 Update Your Profile", "+15 pts", "Fill in your financial profile for better AI recommendations"),
        ("📄 Generate a Report", "+20 pts", "Download your personalized investment PDF report"),
        ("🔥 7-Day Streak", "🎖️ Badge", "Log in for 7 consecutive days to earn Streak Master badge"),
    ]
    
    for action, pts, desc in actions:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; padding:12px; 
             background:rgba(255,255,255,0.04); border-radius:8px; margin-bottom:8px">
            <div style="font-size:1.5rem; min-width:40px">{action.split()[0]}</div>
            <div style="flex:1">
                <div style="color:#fff; font-weight:600">{' '.join(action.split()[1:])}</div>
                <div style="color:#78909c; font-size:0.85rem">{desc}</div>
            </div>
            <div style="color:#ffd54f; font-weight:800; font-size:1.1rem; min-width:80px; text-align:right">{pts}</div>
        </div>
        """, unsafe_allow_html=True)

    # Leaderboard (simulated)
    st.markdown("---")
    st.markdown("### 🏅 Leaderboard (Community)")
    leaderboard = [
        ("🥇 WealthKid99", 842, "Investment Pro"),
        ("🥈 MoneyMind_", 720, "Investment Pro"),
        ("🥉 SIPchamp", 615, "Investment Pro"),
        (f"⭐ {user['username']} (You)", points, level['name']),
        ("💼 InvestorAce", 440, "SIP Starter"),
        ("📊 FinanceFan", 320, "SIP Starter"),
    ]
    
    for rank_str, pts_val, lvl in leaderboard:
        is_you = "You" in rank_str
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; padding:10px 16px;
             background:{'rgba(0,230,118,0.1)' if is_you else 'rgba(255,255,255,0.03)'};
             border-radius:8px; margin-bottom:4px;
             border: {'1px solid #00e676' if is_you else '1px solid transparent'}">
            <div style="color:#fff; font-weight:600; flex:1">{rank_str}</div>
            <div style="color:#78909c; font-size:0.85rem">{lvl}</div>
            <div style="color:#ffd54f; font-weight:800">⭐ {pts_val}</div>
        </div>
        """, unsafe_allow_html=True)
