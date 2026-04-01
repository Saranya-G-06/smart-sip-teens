import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.sip_calculator import calculate_sip, get_yearly_breakdown
from utils.ml_model import predict_sip, get_shap_explanation
from utils.gamification import add_points
from utils.database import get_connection

def save_profile(uid, allowance, savings_rate, risk, goal, horizon, literacy):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO profiles
        (user_id,monthly_allowance,savings_rate,risk_tolerance,investment_goal,investment_horizon,financial_literacy_score)
        VALUES(?,?,?,?,?,?,?)""", (uid,allowance,savings_rate,risk,goal,horizon,literacy))
    conn.commit(); conn.close()

def show_sip_simulator():
    uid = st.session_state.user["id"]
    age = st.session_state.user.get("age", 16)
    PL  = st.session_state.get("PL", {})

    st.markdown("""
    <div style="padding:24px 0 20px 0">
      <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:6px">🤖 Machine Learning + AI</div>
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2rem;color:#141414">SIP Simulator</div>
      <div style="font-size:0.88rem;color:#6B6B6B;font-weight:700;margin-top:4px">Get your AI-powered recommendation, then simulate your wealth growth 💰</div>
    </div>""", unsafe_allow_html=True)

    # ── Profile card ──
    st.markdown("""
    <div style="background:white;border-radius:28px;padding:28px 28px 8px 28px;box-shadow:0 4px 24px rgba(0,0,0,0.08);margin-bottom:4px">
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.1rem;color:#141414;margin-bottom:16px">📋 Your Financial Profile</div>
    </div>""", unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            allowance    = st.slider("💵 Monthly Allowance (₹)", 500, 10000, 2000, 100)
            savings_rate = st.slider("💰 Savings Rate (%)", 5, 80, 30) / 100
        with c2:
            risk    = st.selectbox("⚖️ Risk Tolerance", ["Low","Medium","High"])
            horizon = st.slider("📅 Horizon (years)", 1, 20, 10)
        with c3:
            literacy = st.slider("📚 Literacy Score", 20, 100, 60)
            goal     = st.selectbox("🎯 Goal", ["Education","Gadgets","Travel","Emergency Fund","Wealth"])

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("⚡  Get My AI Recommendation", type="primary"):
            save_profile(uid, allowance, savings_rate, risk, goal, horizon, literacy)
            add_points(uid, 25, "profile")
            st.session_state["show_ml"]   = True
            st.session_state["ml_inputs"] = (allowance, savings_rate, risk, goal, horizon, literacy)
            st.rerun()

    # ── ML Result ──
    if st.session_state.get("show_ml"):
        inp = st.session_state.get("ml_inputs", (allowance, savings_rate, risk, goal, horizon, literacy))
        al, sr, rk, gl, hz, lt = inp
        rec = predict_sip(age, al, sr, lt, hz, rk)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#FFFC00;border-radius:28px;padding:24px;box-shadow:0 6px 0 #E6E300,0 8px 32px rgba(255,252,0,0.3)">
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:0.8rem;text-transform:uppercase;letter-spacing:2px;color:#6B6000;margin-bottom:16px">🤖 AI Recommendation</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
            <div style="text-align:center;padding:12px;background:rgba(0,0,0,0.06);border-radius:16px">
              <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#8B7000;margin-bottom:4px">Recommended SIP</div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.6rem;color:#141414">₹{rec:,.0f}</div>
            </div>
            <div style="text-align:center;padding:12px;background:rgba(0,0,0,0.06);border-radius:16px">
              <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#8B7000;margin-bottom:4px">Monthly Allowance</div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.6rem;color:#141414">₹{al:,}</div>
            </div>
            <div style="text-align:center;padding:12px;background:rgba(0,0,0,0.06);border-radius:16px">
              <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#8B7000;margin-bottom:4px">Savings Rate</div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.6rem;color:#141414">{sr*100:.0f}%</div>
            </div>
            <div style="text-align:center;padding:12px;background:rgba(0,0,0,0.06);border-radius:16px">
              <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#8B7000;margin-bottom:4px">Risk Profile</div>
              <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.6rem;color:#141414">{rk}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # SHAP explanation
        shap_pairs = get_shap_explanation(age, al, sr, lt, hz, rk)
        if shap_pairs:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            se, sc = st.columns([1, 1.5])
            with se:
                items_html = ""
                for feat, val in shap_pairs[:3]:
                    pos = val > 0
                    col   = "#00D084" if pos else "#FF3CA0"
                    bg    = "#E6FFF5" if pos else "#FFE8F5"
                    arrow = "↑" if pos else "↓"
                    label = "Boosting your SIP" if pos else "Limiting your SIP"
                    items_html += f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:{bg};border-radius:12px;margin:5px 0">
                      <div style="font-size:1.1rem;font-weight:900;color:{col}">{arrow}</div>
                      <div>
                        <div style="font-weight:900;font-size:0.82rem;color:#141414">{feat}</div>
                        <div style="font-size:0.72rem;color:#6B6B6B;font-weight:700">{label}</div>
                      </div>
                    </div>"""
                st.markdown(f"""
                <div style="background:white;border-radius:24px;padding:20px;box-shadow:0 4px 20px rgba(0,0,0,0.08)">
                  <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:0.9rem;color:#141414;margin-bottom:12px">🔍 Why this amount?</div>
                  {items_html}
                </div>""", unsafe_allow_html=True)

            with sc:
                fig_s = go.Figure(go.Bar(
                    x=[abs(v) for _, v in shap_pairs],
                    y=[f for f, _ in shap_pairs],
                    orientation="h",
                    marker=dict(color=["#FFFC00" if v>0 else "#FF3CA0" for _,v in shap_pairs], line=dict(width=0)),
                    text=[f"{'+'if v>0 else ''}{v:.1f}" for _,v in shap_pairs],
                    textfont=dict(size=10, color="#141414"), textposition="outside",
                ))
                layout_s = {**PL, "height":220, "showlegend":False,
                    "xaxis":{**PL.get("xaxis",{}), "title":"Impact"}, "bargap":0.38}
                fig_s.update_layout(**layout_s)
                st.plotly_chart(fig_s, use_container_width=True, config={"displayModeBar":False})

        st.session_state["sim_sip"] = rec

    # ── Growth Simulator ──
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:white;border-radius:28px;padding:28px 28px 8px 28px;box-shadow:0 4px 24px rgba(0,0,0,0.08);margin-bottom:4px">
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.1rem;color:#141414;margin-bottom:16px">📊 Growth Simulator</div>
    </div>""", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1: sim_sip = st.number_input("Monthly SIP (₹)", 100, 50000, int(st.session_state.get("sim_sip", 500)), 100)
    with s2: ret     = st.slider("Annual Return (%)", 6.0, 25.0, 12.0, 0.5)
    with s3: yrs     = st.slider("Duration (years)", 1, 30, 10)

    fv, invested, profit = calculate_sip(sim_sip, ret, yrs)
    gain_pct = profit / invested * 100 if invested else 0

    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Total Invested",  f"₹{invested:,.0f}", "#141414", "#F2F2F2"),
        ("Future Value",    f"₹{fv:,.0f}",       "#6B6000", "#FFFBCC"),
        ("Total Profit",    f"₹{profit:,.0f}",   "#007A47", "#E6FFF5"),
        ("Return %",        f"{gain_pct:.1f}%",  "#005A8C", "#E8F7FF"),
    ]
    for col, (lbl, val, color, bg) in zip([m1,m2,m3,m4], metrics):
        col.markdown(f"""
        <div style="background:{bg};border-radius:20px;padding:16px;text-align:center">
          <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#6B6B6B;margin-bottom:6px">{lbl}</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.4rem;color:{color}">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    bd = get_yearly_breakdown(sim_sip, ret, yrs)
    df = pd.DataFrame(bd)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["year"], y=df["invested"], name="Invested",
        marker=dict(color="#E8E8E8", line=dict(width=0)), width=0.55))
    fig.add_trace(go.Bar(x=df["year"], y=df["profit"], name="Returns",
        marker=dict(color="#FFFC00", line=dict(width=0)), width=0.55))
    fig.add_trace(go.Scatter(x=df["year"], y=df["value"], name="Portfolio Value",
        mode="lines+markers", line=dict(color="#FF6B35", width=2.5),
        marker=dict(size=6, color="#FF6B35", line=dict(color="white", width=2))))
    layout_b = {**PL, "barmode":"stack", "height":310, "showlegend":True,
        "xaxis":{**PL.get("xaxis",{}), "title":"Year"},
        "yaxis":{**PL.get("yaxis",{}), "title":"Amount (₹)"}}
    fig.update_layout(**layout_b)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
