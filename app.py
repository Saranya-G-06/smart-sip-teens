import streamlit as st
from utils.database import init_db
from utils.auth import signup_user, login_user, update_streak

st.set_page_config(
    page_title="SmartSIP · Teen Finance",
    page_icon="💛",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@400;600;700&display=swap');

:root {
  --yellow:    #FFFC00;
  --yellow-dk: #E6E300;
  --snap-bg:   #FFFFFF;
  --dark:      #0E0E0E;
  --gray:      #F2F2F2;
  --gray2:     #E8E8E8;
  --gray3:     #C8C8C8;
  --text:      #141414;
  --subtext:   #6B6B6B;
  --ghost:     rgba(0,0,0,0.04);
  --blue:      #0FABFF;
  --pink:      #FF3CA0;
  --green:     #00D084;
  --orange:    #FF6B35;
  --purple:    #8B5CF6;
  --r-sm:      12px;
  --r-md:      20px;
  --r-lg:      28px;
  --r-xl:      40px;
  --r-full:    999px;
  --shadow:    0 4px 24px rgba(0,0,0,0.10);
  --shadow-lg: 0 8px 40px rgba(0,0,0,0.14);
}

*, *::before, *::after { box-sizing: border-box; margin:0; padding:0; }

html, body, [class*="css"], .stApp {
  font-family: 'Nunito', sans-serif !important;
  background: var(--snap-bg) !important;
  color: var(--text) !important;
}

.stApp {
  background: #FAFAFA !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--dark) !important;
  border-right: none !important;
  width: 260px !important;
}
section[data-testid="stSidebar"] > div {
  background: var(--dark) !important;
  padding: 0 !important;
}

/* ── Headings ── */
h1,h2,h3 {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 900 !important;
  color: var(--text) !important;
}
h4,h5,h6,p,span,label,div {
  font-family: 'Nunito Sans', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.3px !important;
  border: none !important;
  border-radius: var(--r-full) !important;
  padding: 11px 28px !important;
  transition: all 0.18s cubic-bezier(0.34,1.56,0.64,1) !important;
  background: var(--yellow) !important;
  color: var(--dark) !important;
  box-shadow: 0 3px 0 var(--yellow-dk), var(--shadow) !important;
}
.stButton > button:hover {
  transform: translateY(-3px) scale(1.03) !important;
  box-shadow: 0 6px 0 var(--yellow-dk), var(--shadow-lg) !important;
}
.stButton > button:active {
  transform: translateY(1px) !important;
  box-shadow: 0 1px 0 var(--yellow-dk) !important;
}
button[kind="secondary"], .stButton > button[kind="secondary"] {
  background: var(--gray) !important;
  color: var(--text) !important;
  box-shadow: 0 3px 0 var(--gray2), 0 2px 8px rgba(0,0,0,0.06) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: var(--gray) !important;
  border: 2.5px solid transparent !important;
  border-radius: var(--r-md) !important;
  color: var(--text) !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  padding: 12px 16px !important;
  transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--yellow) !important;
  background: white !important;
  box-shadow: 0 0 0 4px rgba(255,252,0,0.2) !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1.2px !important;
  color: var(--subtext) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: var(--gray) !important;
  border: 2.5px solid transparent !important;
  border-radius: var(--r-md) !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 700 !important;
  color: var(--text) !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--yellow) !important;
  box-shadow: 0 0 0 4px rgba(255,252,0,0.2) !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] div[role="slider"] {
  background: var(--dark) !important;
  border: 3px solid var(--yellow) !important;
  width: 22px !important; height: 22px !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}
div[data-testid="stSlider"] [data-testid="stSliderTrack"] > span:first-child {
  background: var(--dark) !important;
  height: 5px !important;
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
  background: white !important;
  border-radius: var(--r-lg) !important;
  border: none !important;
  box-shadow: var(--shadow) !important;
  padding: 18px !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
}
div[data-testid="metric-container"]:hover {
  transform: translateY(-3px) !important;
  box-shadow: var(--shadow-lg) !important;
}
div[data-testid="metric-container"] label {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1.2px !important;
  color: var(--subtext) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] div {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 900 !important;
  font-size: 1.8rem !important;
  color: var(--dark) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--gray) !important;
  border-radius: var(--r-full) !important;
  padding: 5px !important;
  gap: 3px !important;
  border: none !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--subtext) !important;
  border-radius: var(--r-full) !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.85rem !important;
  padding: 9px 22px !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--dark) !important;
  color: var(--yellow) !important;
  box-shadow: var(--shadow) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display:none !important; }

/* ── Expander ── */
.stExpander {
  background: white !important;
  border: none !important;
  border-radius: var(--r-lg) !important;
  box-shadow: var(--shadow) !important;
  overflow: hidden !important;
  margin: 8px 0 !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
}
.stExpander:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-lg) !important;
}
.stExpander > details > summary {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.95rem !important;
  color: var(--text) !important;
  padding: 16px 20px !important;
}

/* ── Progress ── */
.stProgress > div {
  background: var(--gray2) !important;
  border-radius: var(--r-full) !important;
  height: 10px !important;
}
.stProgress > div > div {
  background: linear-gradient(90deg, var(--yellow), var(--orange)) !important;
  border-radius: var(--r-full) !important;
  height: 10px !important;
}

/* ── Alerts ── */
.stSuccess { background:#E6FFF5 !important; border:none !important; border-left:4px solid var(--green) !important; border-radius:var(--r-md) !important; color:#007A47 !important; font-weight:700 !important; }
.stWarning { background:#FFFBCC !important; border:none !important; border-left:4px solid var(--yellow-dk) !important; border-radius:var(--r-md) !important; color:#6B6000 !important; font-weight:700 !important; }
.stError   { background:#FFE8F0 !important; border:none !important; border-left:4px solid var(--pink) !important; border-radius:var(--r-md) !important; color:#B0003A !important; font-weight:700 !important; }
.stInfo    { background:#E8F7FF !important; border:none !important; border-left:4px solid var(--blue) !important; border-radius:var(--r-md) !important; color:#005A8C !important; font-weight:700 !important; }

/* ── Divider ── */
hr { border: none !important; border-top: 2px solid var(--gray2) !important; margin: 20px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--gray); }
::-webkit-scrollbar-thumb { background: var(--gray3); border-radius: 5px; }

/* ── Plotly ── */
.js-plotly-plot .plotly { border-radius: var(--r-lg) !important; }

/* ── Snap Cards ── */
.snap-card {
  background: white;
  border-radius: var(--r-xl);
  box-shadow: var(--shadow);
  padding: 24px;
  transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.22s;
}
.snap-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }

.snap-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--yellow); color: var(--dark);
  border-radius: var(--r-full); padding: 4px 12px;
  font-family: 'Nunito', sans-serif; font-weight: 800;
  font-size: 0.75rem; letter-spacing: 0.5px;
}

.snap-pill {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--gray); color: var(--subtext);
  border-radius: var(--r-full); padding: 5px 14px;
  font-family: 'Nunito', sans-serif; font-weight: 700;
  font-size: 0.8rem;
}

.section-tag {
  font-family: 'Nunito', sans-serif;
  font-weight: 900; font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 2px;
  color: var(--subtext); margin-bottom: 10px;
  display: block;
}

.ghost-row {
  display:flex; justify-content:space-between; align-items:center;
  padding: 12px 16px; background: var(--ghost);
  border-radius: var(--r-md); margin: 5px 0;
}

/* ── Animations ── */
@keyframes popIn {
  0%   { transform: scale(0.85); opacity: 0; }
  70%  { transform: scale(1.04); }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}
@keyframes pulse-ring {
  0%   { box-shadow: 0 0 0 0 rgba(255,252,0,0.6); }
  70%  { box-shadow: 0 0 0 12px rgba(255,252,0,0); }
  100% { box-shadow: 0 0 0 0 rgba(255,252,0,0); }
}

.pop-in  { animation: popIn 0.4s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.slide-up { animation: slideUp 0.35s ease forwards; }
.pulse   { animation: pulse-ring 2s ease infinite; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Shared plotly theme stored in session
st.session_state["PL"] = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Nunito, sans-serif", color="#6B6B6B", size=12),
    legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#E8E8E8",
                borderwidth=1, font=dict(color="#141414", size=11)),
    xaxis=dict(gridcolor="rgba(0,0,0,0.05)", zerolinecolor="rgba(0,0,0,0.08)",
               tickfont=dict(color="#9B9B9B", size=11)),
    yaxis=dict(gridcolor="rgba(0,0,0,0.05)", zerolinecolor="rgba(0,0,0,0.08)",
               tickfont=dict(color="#9B9B9B", size=11)),
    margin=dict(l=8, r=8, t=20, b=8),
)

# ── AUTH ──────────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

def show_auth():
    col_l, col_c, col_r = st.columns([0.8, 1.4, 0.8])
    with col_c:
        # Hero
        st.markdown("""
        <div style="text-align:center;padding:48px 0 32px 0">
          <div style="animation:popIn 0.5s cubic-bezier(0.34,1.56,0.64,1) forwards">
            <div style="font-size:5rem;line-height:1;margin-bottom:16px">💛</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2.6rem;
              color:#141414;line-height:1.1;margin-bottom:10px">SmartSIP</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:800;font-size:1rem;
              color:#6B6B6B;letter-spacing:3px;text-transform:uppercase;margin-bottom:28px">
              Teen Finance · Leveled Up 🚀
            </div>
            <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:36px">
        """ + "".join([f'<span class="snap-pill">{t}</span>' for t in ["🤖 AI-Powered","🎮 Gamified","📊 Simulator","🏅 Badges","📚 Education"]]) + """
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Card
        st.markdown("""
        <div style="background:white;border-radius:32px;padding:32px 28px;
          box-shadow:0 8px 48px rgba(0,0,0,0.12);margin:0 auto">
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["👋  Sign In", "✨  Join Free"])

        with tab1:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            u = st.text_input("Username", key="li_u", placeholder="your_username")
            p = st.text_input("Password", type="password", key="li_p", placeholder="••••••••")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Sign In  →", type="primary", key="li_btn", use_container_width=True):
                if u and p:
                    ok, user = login_user(u, p)
                    if ok:
                        st.session_state.user = user
                        c, h = update_streak(user["id"])
                        st.session_state.streak = (c, h)
                        st.rerun()
                    else:
                        st.error("Wrong credentials. Try demo / demo123")
                else:
                    st.warning("Enter your username and password!")
            st.markdown("""
            <div style="margin-top:16px;background:#FFFBCC;border-radius:16px;
              padding:12px 16px;border-left:4px solid #FFFC00">
              <div style="font-weight:900;font-size:0.78rem;color:#6B6000;
                text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">🎯 Demo Account</div>
              <div style="font-size:0.85rem;color:#8B7000;font-weight:700">
                demo &nbsp;/&nbsp; demo123
              </div>
            </div>""", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            nu = st.text_input("Username", key="su_u", placeholder="pick_a_cool_name")
            ne = st.text_input("Email",    key="su_e", placeholder="you@email.com")
            np = st.text_input("Password", type="password", key="su_p", placeholder="Min 6 chars")
            na = st.number_input("Age", 13, 19, 16, key="su_a")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Create Account  →", type="primary", key="su_btn", use_container_width=True):
                if nu and ne and np and len(np) >= 6:
                    ok, msg = signup_user(nu, ne, np, na)
                    st.success("Account created! Sign in now 🎉") if ok else st.error(msg)
                else:
                    st.warning("All fields required (password ≥ 6 chars)")

        # Feature grid
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        fc = st.columns(4)
        feats = [
            ("#FFFC00","🤖","AI SIP Advisor","Trained ML Model"),
            ("#FFE8F7","📊","Growth Simulator","Interactive Charts"),
            ("#E8F7FF","🎮","Earn Badges","5 Levels of XP"),
            ("#E6FFF5","📚","8 Lessons","Learn & Earn Pts"),
        ]
        for col,(bg,icon,t,s) in zip(fc, feats):
            col.markdown(f"""
            <div style="background:{bg};border-radius:24px;padding:20px 16px;text-align:center;
              transition:transform 0.2s;cursor:default" class="snap-card">
              <div style="font-size:2rem;margin-bottom:8px">{icon}</div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;
                font-size:0.85rem;color:#141414;margin-bottom:4px">{t}</div>
              <div style="font-size:0.75rem;color:#6B6B6B;font-weight:700">{s}</div>
            </div>""", unsafe_allow_html=True)

def create_demo_user():
    try: signup_user("demo","demo@smartsip.com","demo123",17)
    except: pass

create_demo_user()

if st.session_state.user is None:
    show_auth()
else:
    user = st.session_state.user

    # ── SIDEBAR ──────────────────────────────────────────────────────────
    with st.sidebar:
        streak  = st.session_state.get("streak", (0, 0))
        initial = user['username'][0].upper()
        age_val = user.get('age', '—')

        st.markdown(f"""
        <div style="padding:24px 16px 16px 16px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px">
            <div style="width:40px;height:40px;background:#FFFC00;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;box-shadow:0 3px 0 #E6E300">&#x1F49B;</div>
            <div>
              <div style="font-weight:900;font-size:1rem;color:white">SmartSIP</div>
              <div style="font-size:0.6rem;color:#555;letter-spacing:2px;text-transform:uppercase;font-weight:700">Teen Finance</div>
            </div>
          </div>
          <div style="background:rgba(255,255,255,0.05);border-radius:18px;padding:14px;margin-bottom:16px">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
              <div style="width:42px;height:42px;background:#FFFC00;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1rem;font-weight:900;color:#141414">{initial}</div>
              <div>
                <div style="font-weight:900;font-size:0.9rem;color:white">{user['username']}</div>
                <div style="font-size:0.72rem;color:#555;font-weight:700">Age {age_val}</div>
              </div>
            </div>
            <div style="display:flex;gap:8px">
              <div style="flex:1;background:rgba(255,252,0,0.12);border-radius:10px;padding:8px;text-align:center">
                <div style="font-size:1rem">&#x1F525;</div>
                <div style="color:#FFFC00;font-weight:900;font-size:0.85rem">{streak[0]}d</div>
                <div style="color:#444;font-size:0.6rem;font-weight:700">STREAK</div>
              </div>
              <div style="flex:1;background:rgba(255,255,255,0.05);border-radius:10px;padding:8px;text-align:center">
                <div style="font-size:1rem">&#x1F3C6;</div>
                <div style="color:white;font-weight:900;font-size:0.85rem">{streak[1]}d</div>
                <div style="color:#444;font-size:0.6rem;font-weight:700">BEST</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if "current_page" not in st.session_state:
            st.session_state.current_page = "dashboard"

        NAV = [
            ("dashboard",     "📊", "Dashboard"),
            ("sip_simulator", "🤖", "SIP Simulator"),
            ("advisor",       "💬", "AI Advisor"),
            ("education",     "📚", "Education"),
            ("gamification",  "🎮", "Gamification"),
            ("report",        "📄", "Reports"),
        ]

        st.markdown("<div style='padding:0 12px'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.65rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#444;padding:0 8px;margin-bottom:8px'>Navigation</div>", unsafe_allow_html=True)

        for pid, icon, label in NAV:
            active = st.session_state.current_page == pid
            if active:
                # Active item: show styled div only, no button (avoids text overlap)
                st.markdown(f"""
                <div style="background:#FFFC00;border-radius:14px;padding:11px 16px;
                  margin:4px 0;display:flex;align-items:center;gap:10px;
                  box-shadow:0 3px 0 #E6E300">
                  <span style="font-size:1.1rem">{icon}</span>
                  <span style="font-family:'Nunito',sans-serif;font-weight:900;
                    font-size:0.88rem;color:#141414">{label}</span>
                </div>""", unsafe_allow_html=True)
            else:
                # Inactive items: clickable button only
                if st.button(f"{icon}  {label}", key=f"nav_{pid}", use_container_width=True):
                    st.session_state.current_page = pid
                    st.rerun()

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("👋  Sign Out", use_container_width=True):
            for k in ["user","current_page","chat_history","show_ml","streak","sim_sip","ml_inputs"]:
                st.session_state.pop(k, None)
            st.rerun()

        st.markdown("""
        <div style="position:absolute;bottom:20px;left:0;right:0;text-align:center;
          font-size:0.7rem;color:#333;font-weight:700">
          Made with 💛 for teens
        </div>""", unsafe_allow_html=True)

    # ── PAGE ROUTING ──────────────────────────────────────────────────────
    pg = st.session_state.current_page
    if   pg == "dashboard":     from pages.dashboard       import show_dashboard;     show_dashboard()
    elif pg == "sip_simulator": from pages.sip_simulator   import show_sip_simulator; show_sip_simulator()
    elif pg == "advisor":       from pages.advisor         import show_advisor;       show_advisor()
    elif pg == "education":     from pages.education       import show_education;     show_education()
    elif pg == "gamification":  from pages.gamification_page import show_gamification; show_gamification()
    elif pg == "report":        from pages.report          import show_report;        show_report()