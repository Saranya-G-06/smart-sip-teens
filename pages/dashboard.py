import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.auth import get_streak
from utils.gamification import get_gamification, BADGES
from utils.sip_calculator import get_yearly_breakdown
from utils.database import get_connection

def get_profile(uid):
    c = get_connection().cursor()
    c.execute("SELECT * FROM profiles WHERE user_id=?", (uid,))
    return c.fetchone()

def show_dashboard():
    user    = st.session_state.user
    uid     = user["id"]
    PL      = st.session_state.get("PL", {})
    streak  = get_streak(uid)
    gami    = get_gamification(uid)
    profile = get_profile(uid)

    # ── Page header ──
    st.markdown(f"""
    <div style="padding:24px 0 20px 0">
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:4px">
        <div style="width:52px;height:52px;background:#FFFC00;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:900;color:#141414;box-shadow:0 4px 0 #E6E300">
          {user['username'][0].upper()}
        </div>
        <div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.6rem;color:#141414;line-height:1">Hey, {user['username']}! 👋</div>
          <div style="font-size:0.85rem;color:#6B6B6B;font-weight:700">Here's your financial snapshot today</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── KPI row ──
    k1, k2, k3, k4, k5 = st.columns(5)
    kpis = [
        ("🔥","#FFFC00","#FFFBCC","Streak",      f"{streak[0]}d",          "days active"),
        ("🏆","#0FABFF","#E8F7FF","Best Streak",  f"{streak[1]}d",          "personal record"),
        ("⭐","#8B5CF6","#F0EBFF","Points",       f"{gami['points']:,}",    "xp earned"),
        ("📚","#00D084","#E6FFF5","Lessons",      f"{len(gami['lessons'])}/8","done"),
        ("🏅","#FF6B35","#FFF0EB","Badges",       f"{len(gami['badges'])}","unlocked"),
    ]
    for col, (icon, accent, bg, lbl, val, sub) in zip([k1,k2,k3,k4,k5], kpis):
        col.markdown(f"""
        <div style="background:white;border-radius:24px;padding:18px 14px;box-shadow:0 4px 20px rgba(0,0,0,0.08);text-align:center">
          <div style="width:44px;height:44px;background:{bg};border-radius:16px;margin:0 auto 10px auto;display:flex;align-items:center;justify-content:center;font-size:1.3rem">{icon}</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.7rem;color:{accent};line-height:1;margin-bottom:4px">{val}</div>
          <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#9B9B9B;margin-bottom:2px">{lbl}</div>
          <div style="font-size:0.7rem;color:#C8C8C8;font-weight:700">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if profile:
        _, allowance, savings_rate, risk, goal, horizon, literacy = profile
        monthly_sip = allowance * savings_rate
        breakdown   = get_yearly_breakdown(monthly_sip, 12, int(horizon or 10))
        df          = pd.DataFrame(breakdown)
        final       = breakdown[-1] if breakdown else {}

        cl, cr = st.columns([1.7, 1], gap="large")

        with cl:
            st.markdown("<div style='font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:8px'>📈 Investment Trajectory</div>", unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["year"], y=df["value"], name="Portfolio Value",
                mode="lines", line=dict(color="#FFFC00", width=3),
                fill="tozeroy", fillcolor="rgba(255,252,0,0.08)"
            ))
            fig.add_trace(go.Scatter(
                x=df["year"], y=df["invested"], name="Invested",
                mode="lines", line=dict(color="#0FABFF", width=2, dash="dot"),
            ))
            layout = {**PL, "height": 270, "showlegend": True,
                "xaxis": {**PL.get("xaxis",{}), "title": "Year"},
                "yaxis": {**PL.get("yaxis",{}), "title": "₹ Value"}}
            fig.update_layout(**layout)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with cr:
            st.markdown("<div style='font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:8px'>🥧 Portfolio Mix</div>", unsafe_allow_html=True)
            alloc = {"Low":[40,50,10],"Medium":[60,30,10],"High":[80,15,5]}
            vals  = alloc.get(risk, [60,30,10])
            fig2  = go.Figure(go.Pie(
                labels=["Equity","Debt","Gold"], values=vals, hole=0.65,
                marker=dict(colors=["#FFFC00","#0FABFF","#FF6B35"], line=dict(color="white", width=3)),
                textfont=dict(size=11, color="#6B6B6B"),
            ))
            layout2 = {**PL, "height": 210, "showlegend": True,
                "annotations":[dict(text=f"<b>{risk}</b><br>Risk", x=0.5, y=0.5,
                    font_size=13, font_color="#141414", showarrow=False)]}
            fig2.update_layout(**layout2)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

            for lbl, val, color in [
                ("Monthly SIP",    f"₹{monthly_sip:,.0f}", "#141414"),
                ("Projected Value",f"₹{final.get('value',0):,.0f}", "#00D084"),
                ("Est. Returns",   f"₹{final.get('profit',0):,.0f}", "#0FABFF"),
            ]:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 14px;background:#F7F7F7;border-radius:12px;margin:4px 0">
                  <span style="font-size:0.8rem;color:#6B6B6B;font-weight:700">{lbl}</span>
                  <span style="font-weight:900;font-size:0.9rem;color:{color}">{val}</span>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#FFFBCC;border-radius:28px;padding:32px;text-align:center;border:3px dashed #FFFC00;margin:16px 0">
          <div style="font-size:3rem;margin-bottom:12px">🚀</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.3rem;color:#141414;margin-bottom:8px">Set Up Your Profile!</div>
          <div style="color:#6B6B6B;font-size:0.9rem;font-weight:700;max-width:340px;margin:0 auto">Head to SIP Simulator to get your AI recommendation and unlock your full dashboard!</div>
        </div>""", unsafe_allow_html=True)

    # ── Badges ──
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:8px'>🏅 Badge Collection</div>", unsafe_allow_html=True)
    earned = gami["badges"]
    bc = st.columns(len(BADGES))
    badge_colors = {"Beginner Investor":"#00D084","SIP Starter":"#0FABFF","Investment Pro":"#FF6B35","Streak Master":"#FFFC00"}

    for i, (badge, info) in enumerate(BADGES.items()):
        unlocked = badge in earned
        color    = badge_colors.get(badge, "#FFFC00")
        earned_tag = f'<div style="background:{color};color:#141414;font-size:0.65rem;font-weight:900;padding:3px 10px;border-radius:999px;display:inline-block;margin-top:6px">EARNED ✓</div>' if unlocked else ''
        with bc[i]:
            st.markdown(f"""
            <div style="background:{'white' if unlocked else '#F2F2F2'};border-radius:24px;padding:20px 14px;text-align:center;
              box-shadow:{'0 4px 20px rgba(0,0,0,0.10)' if unlocked else 'none'};
              border:{'3px solid '+color if unlocked else '3px dashed #E8E8E8'};
              opacity:{'1' if unlocked else '0.5'}">
              <div style="font-size:2.2rem;margin-bottom:8px">{'🔒' if not unlocked else info['icon']}</div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:0.78rem;color:{'#141414' if unlocked else '#9B9B9B'};margin-bottom:4px">{badge}</div>
              <div style="font-size:0.7rem;color:#9B9B9B;font-weight:700">{info['desc']}</div>
              {earned_tag}
            </div>""", unsafe_allow_html=True)
