import streamlit as st
from utils.gamification import get_gamification, BADGES, add_points
from utils.auth import get_streak

LEVELS = [
    (0,    "Newbie",      "🐣", "#C8C8C8"),
    (100,  "Learner",     "📖", "#0FABFF"),
    (300,  "Saver",       "💰", "#00D084"),
    (600,  "Investor",    "📊", "#FF6B35"),
    (1000, "Pro Trader",  "🚀", "#FFFC00"),
]
HOW_TO = [
    ("📅","#FFFBCC","#FFFC00",  "Daily Login",       10, "Log in every day"),
    ("📚","#E6FFF5","#00D084",  "Complete Lesson",   50, "Finish any lesson"),
    ("💰","#E8F7FF","#0FABFF",  "SIP Simulator",     25, "Run a simulation"),
    ("💬","#F0EBFF","#8B5CF6",  "AI Advisor Chat",    5, "Ask a question"),
    ("✏️","#FFF0EB","#FF6B35",  "Update Profile",    25, "Keep profile fresh"),
]

def show_gamification():
    uid = st.session_state.user["id"]
    gami   = get_gamification(uid)
    streak = get_streak(uid)
    points = gami["points"]

    st.markdown("""
    <div style="padding:24px 0 20px 0" class="slide-up">
      <div class="section-tag">🎮 Rewards & Progress</div>
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2rem;color:#141414">
        Gamification
      </div>
      <div style="font-size:0.88rem;color:#6B6B6B;font-weight:700;margin-top:4px">
        Earn points, unlock badges, and level up your investing game 💪
      </div>
    </div>""", unsafe_allow_html=True)

    # Current level
    cur_lv = LEVELS[0]; nxt_lv = LEVELS[1]
    for i,lv in enumerate(LEVELS):
        if points >= lv[0]:
            cur_lv = lv
            nxt_lv = LEVELS[i+1] if i+1<len(LEVELS) else lv
    nxt_thresh = nxt_lv[0] if nxt_lv!=cur_lv else points
    prog = min(points/nxt_thresh,1.0) if nxt_thresh>0 else 1.0

    # Level hero
    st.markdown(f"""
    <div style="background:#141414;border-radius:28px;padding:28px;margin-bottom:20px;
      color:white;position:relative;overflow:hidden">
      <div style="position:absolute;top:-30px;right:-30px;width:140px;height:140px;
        background:{cur_lv[3]};border-radius:50%;opacity:0.12"></div>
      <div style="position:absolute;bottom:-20px;left:40%;width:80px;height:80px;
        background:{nxt_lv[3]};border-radius:50%;opacity:0.08"></div>
      <div style="display:flex;align-items:center;justify-content:space-between;
        flex-wrap:wrap;gap:20px;position:relative">
        <div>
          <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;
            letter-spacing:2px;color:#555;margin-bottom:8px">Current Level</div>
          <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:3rem">{cur_lv[2]}</div>
            <div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.8rem;
                color:{cur_lv[3]}">{cur_lv[1]}</div>
              <div style="color:#555;font-size:0.82rem;font-weight:700">
                {points:,} XP earned
              </div>
            </div>
          </div>
        </div>
        <div style="flex:1;min-width:180px">
          <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="color:#555;font-size:0.78rem;font-weight:700">
              → {nxt_lv[1]}
            </span>
            <span style="color:white;font-size:0.78rem;font-weight:900;
              font-family:'Nunito',sans-serif">
              {points:,}/{nxt_thresh:,} XP
            </span>
          </div>
          <div style="background:rgba(255,255,255,0.1);border-radius:999px;height:10px">
            <div style="width:{prog*100:.1f}%;height:100%;
              background:linear-gradient(90deg,{cur_lv[3]},{nxt_lv[3]});
              border-radius:999px"></div>
          </div>
        </div>
        <div style="text-align:center">
          <div style="font-size:2rem">🔥</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;
            font-size:1.5rem;color:white">{streak[0]}d</div>
          <div style="font-size:0.68rem;color:#555;font-weight:700">STREAK</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    cl, cr = st.columns([1.1,1], gap="large")

    with cl:
        st.markdown("<div class='section-tag'>🏅 Badge Collection</div>", unsafe_allow_html=True)
        earned = gami["badges"]
        badge_colors = {"Beginner Investor":"#00D084","SIP Starter":"#0FABFF",
                        "Investment Pro":"#FF6B35","Streak Master":"#FFFC00"}
        for badge,info in BADGES.items():
            unlocked = badge in earned
            color    = badge_colors.get(badge,"#FFFC00")
            if unlocked:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:14px;padding:14px 18px;
                  background:white;border-radius:20px;margin:6px 0;
                  box-shadow:0 3px 16px rgba(0,0,0,0.08);
                  border-left:5px solid {color}">
                  <div style="font-size:2rem">{info['icon']}</div>
                  <div style="flex:1">
                    <div style="font-family:'Nunito',sans-serif;font-weight:900;
                      font-size:0.9rem;color:#141414">{badge}</div>
                    <div style="font-size:0.75rem;color:#6B6B6B;font-weight:700">{info['desc']}</div>
                  </div>
                  <div style="background:{color};color:#141414;font-size:0.7rem;
                    font-weight:900;padding:4px 12px;border-radius:999px">EARNED ✓</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:14px;padding:14px 18px;
                  background:#F7F7F7;border-radius:20px;margin:6px 0;
                  border:2px dashed #E8E8E8;opacity:0.55">
                  <div style="font-size:2rem">🔒</div>
                  <div style="flex:1">
                    <div style="font-weight:900;font-size:0.9rem;color:#9B9B9B">{badge}</div>
                    <div style="font-size:0.75rem;color:#C8C8C8;font-weight:700">{info['desc']}</div>
                  </div>
                  <div style="color:#C8C8C8;font-size:0.7rem;font-weight:900">LOCKED</div>
                </div>""", unsafe_allow_html=True)

    with cr:
        st.markdown("<div class='section-tag'>💡 How to Earn Points</div>", unsafe_allow_html=True)
        for icon,bg,accent,name,pts,desc in HOW_TO:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:12px 14px;
              background:white;border-radius:16px;margin:5px 0;
              box-shadow:0 2px 10px rgba(0,0,0,0.06)">
              <div style="width:40px;height:40px;min-width:40px;background:{bg};
                border-radius:14px;display:flex;align-items:center;justify-content:center;
                font-size:1.1rem;border:2px solid {accent}">{icon}</div>
              <div style="flex:1">
                <div style="font-weight:900;font-size:0.85rem;color:#141414">{name}</div>
                <div style="font-size:0.72rem;color:#9B9B9B;font-weight:700">{desc}</div>
              </div>
              <div style="background:{bg};color:{accent};font-weight:900;font-size:1rem;
                padding:5px 12px;border-radius:999px;border:2px solid {accent}">+{pts}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-tag'>📊 All Levels</div>", unsafe_allow_html=True)
        for thresh,name,icon,color in LEVELS:
            reached = points >= thresh
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;
              border-radius:12px;background:{'white' if reached else 'transparent'};
              opacity:{'1' if reached else '0.4'};margin:3px 0;
              box-shadow:{'0 2px 8px rgba(0,0,0,0.06)' if reached else 'none'}">
              <span style="font-size:1.1rem">{icon}</span>
              <span style="flex:1;font-weight:900;font-size:0.85rem;
                color:{'#141414' if reached else '#9B9B9B'}">{name}</span>
              <span style="color:{color if reached else '#C8C8C8'};font-weight:900;
                font-size:0.78rem">{thresh:,} XP</span>
              {'<span style="color:#00D084;font-weight:900;font-size:0.75rem">✓</span>' if reached else ''}
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("🎁  Claim Daily Bonus (+10 pts)", type="primary", use_container_width=True):
            add_points(uid,10,"bonus")
            st.success("🎉 +10 XP added!"); st.rerun()
