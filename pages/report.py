import streamlit as st
import io
from utils.database import get_connection
from utils.sip_calculator import calculate_sip, get_yearly_breakdown
from utils.gamification import get_gamification
from utils.auth import get_streak

def get_profile(uid):
    c = get_connection().cursor()
    c.execute("SELECT * FROM profiles WHERE user_id=?", (uid,))
    return c.fetchone()

def generate_pdf(user, profile, gami, streak):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.colors import HexColor, white
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.units import cm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
            topMargin=1.5*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
        story = []

        YELLOW = HexColor("#FFFC00"); DARK = HexColor("#0E0E0E")
        BLUE   = HexColor("#0FABFF"); GREEN = HexColor("#00D084")
        LIGHT  = HexColor("#F7F7F7"); GRAY  = HexColor("#6B6B6B")

        def ps(name, **kw): return ParagraphStyle(name, fontName="Helvetica", **kw)

        hdr = [[
            Paragraph('<font color="#0E0E0E" size="22"><b>SmartSIP</b></font><br/><font color="#6B6B6B" size="8">TEEN FINANCE · INVESTMENT REPORT</font>', ps("h")),
            Paragraph(f'<font color="#6B6B6B" size="7">GENERATED FOR</font><br/><font color="#0E0E0E" size="14"><b>{user["username"].upper()}</b></font><br/><font color="#6B6B6B" size="8">Age {user.get("age","—")} · Streak: {streak[0]} days</font>', ps("h2", alignment=2))
        ]]
        ht = Table(hdr, colWidths=[9.5*cm, 9.5*cm])
        ht.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),YELLOW),
            ("TOPPADDING",(0,0),(-1,-1),18),("BOTTOMPADDING",(0,0),(-1,-1),18),
            ("LEFTPADDING",(0,0),(0,-1),18),("RIGHTPADDING",(-1,0),(-1,-1),18),
        ]))
        story.append(ht); story.append(Spacer(1, 0.5*cm))

        def sec(t): return Paragraph(f'<font color="#9B9B9B" size="7"><b>{t}</b></font>', ps("s", spaceBefore=12, spaceAfter=6))

        if profile:
            _, al, sr, risk, goal, hz, lit = profile
            sip = al * sr
            fv, invested, profit = calculate_sip(sip, 12, hz or 10)

            story.append(sec("KEY NUMBERS"))
            kpis = [[
                Paragraph(f'<font color="#6B6B6B" size="7">MONTHLY SIP</font><br/><font color="#0E0E0E" size="20"><b>₹{sip:,.0f}</b></font>', ps("k", alignment=1)),
                Paragraph(f'<font color="#6B6B6B" size="7">PROJECTED VALUE</font><br/><font color="#0FABFF" size="20"><b>₹{fv:,.0f}</b></font>', ps("k", alignment=1)),
                Paragraph(f'<font color="#6B6B6B" size="7">TOTAL RETURNS</font><br/><font color="#00D084" size="20"><b>₹{profit:,.0f}</b></font>', ps("k", alignment=1)),
                Paragraph(f'<font color="#6B6B6B" size="7">RETURN RATE</font><br/><font color="#FF6B35" size="20"><b>{profit/invested*100:.1f}%</b></font>', ps("k", alignment=1)),
            ]]
            kt = Table(kpis, colWidths=[4.75*cm]*4)
            kt.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1),LIGHT),
                ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
                ("GRID",(0,0),(-1,-1),1,white),
            ]))
            story.append(kt); story.append(Spacer(1, 0.4*cm))

            story.append(sec("FINANCIAL PROFILE"))
            pd_data = [
                ["Parameter","Value","Parameter","Value"],
                ["Monthly Allowance",f"₹{al:,.0f}","Risk Tolerance",str(risk)],
                ["Savings Rate",f"{sr*100:.0f}%","Investment Goal",str(goal)],
                ["Horizon",f"{hz} years","Literacy Score",str(lit)],
                ["Streak",f"{streak[0]} days","XP Points",f"{gami['points']:,}"],
            ]
            pt = Table(pd_data, colWidths=[5*cm,4*cm,5*cm,5*cm])
            pt.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),DARK),
                ("TEXTCOLOR",(0,0),(-1,0),YELLOW),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                ("FONTSIZE",(0,0),(-1,0),8),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT,white]),
                ("TEXTCOLOR",(0,1),(-1,-1),HexColor("#141414")),
                ("FONTSIZE",(0,1),(-1,-1),9),
                ("GRID",(0,0),(-1,-1),0.5,HexColor("#E8E8E8")),
                ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
                ("LEFTPADDING",(0,0),(-1,-1),10),
            ]))
            story.append(pt); story.append(Spacer(1, 0.4*cm))

            story.append(sec("YEAR-BY-YEAR PROJECTION"))
            proj = [["Year","Invested (₹)","Portfolio (₹)","Returns (₹)","Return %"]]
            for row in get_yearly_breakdown(sip, 12, hz or 10):
                if row["year"] in [1,2,3,5,7,10] or row["year"] == (hz or 10):
                    proj.append([str(row["year"]), f"{row['invested']:,.0f}",
                        f"{row['value']:,.0f}", f"{row['profit']:,.0f}",
                        f"{row['profit']/row['invested']*100:.1f}%"])
            pt2 = Table(proj, colWidths=[2*cm,4*cm,5*cm,4.5*cm,3.5*cm])
            pt2.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),DARK),
                ("TEXTCOLOR",(0,0),(-1,0),YELLOW),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                ("FONTSIZE",(0,0),(-1,0),8),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT,white]),
                ("TEXTCOLOR",(0,1),(-1,-1),HexColor("#141414")),
                ("TEXTCOLOR",(2,1),(-1,-1),BLUE),
                ("FONTSIZE",(0,1),(-1,-1),9),
                ("GRID",(0,0),(-1,-1),0.5,HexColor("#E8E8E8")),
                ("ALIGN",(1,0),(-1,-1),"RIGHT"),
                ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
                ("LEFTPADDING",(0,0),(-1,-1),8),
            ]))
            story.append(pt2)

        story.append(Spacer(1, 0.6*cm))
        story.append(HRFlowable(width="100%", thickness=2, color=YELLOW))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph('<font color="#9B9B9B" size="7">SmartSIP for Teens · Start Early. Grow Rich.</font>', ps("footer", alignment=1)))

        doc.build(story)
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        return None

def show_report():
    uid     = st.session_state.user["id"]
    user    = st.session_state.user
    profile = get_profile(uid)
    gami    = get_gamification(uid)
    streak  = get_streak(uid)

    st.markdown("""
    <div style="padding:24px 0 20px 0">
      <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:6px">📄 Export</div>
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2rem;color:#141414">Investment Report</div>
      <div style="font-size:0.88rem;color:#6B6B6B;font-weight:700;margin-top:4px">Download your personalized PDF report with projections, profile and achievements</div>
    </div>""", unsafe_allow_html=True)

    if not profile:
        st.markdown("""
        <div style="background:#FFFBCC;border-radius:24px;padding:28px;text-align:center;border:3px dashed #FFFC00">
          <div style="font-size:2.5rem;margin-bottom:10px">⚠️</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.1rem;color:#141414;margin-bottom:6px">Profile Required!</div>
          <div style="color:#6B6000;font-size:0.9rem;font-weight:700">Set up your profile in the SIP Simulator first, then come back here.</div>
        </div>""", unsafe_allow_html=True)
        return

    _, al, sr, risk, goal, hz, lit = profile
    sip = al * sr
    fv, invested, profit = calculate_sip(sip, 12, hz or 10)

    # Preview — fully self-contained HTML block
    st.markdown(f"""
    <div style="background:#141414;border-radius:28px;padding:28px;margin-bottom:20px;position:relative;overflow:hidden">
      <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;background:#FFFC00;border-radius:50%;opacity:0.06"></div>
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1rem;color:#FFFC00;margin-bottom:20px;letter-spacing:1px">📊 REPORT PREVIEW</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
        <div style="background:rgba(255,255,255,0.06);border-radius:18px;padding:16px;text-align:center;border:1px solid rgba(255,255,255,0.1)">
          <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#555;margin-bottom:8px">Monthly SIP</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.4rem;color:#FFFC00">₹{sip:,.0f}</div>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:18px;padding:16px;text-align:center;border:1px solid rgba(255,255,255,0.1)">
          <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#555;margin-bottom:8px">Projected Value</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.4rem;color:#0FABFF">₹{fv:,.0f}</div>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:18px;padding:16px;text-align:center;border:1px solid rgba(255,255,255,0.1)">
          <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#555;margin-bottom:8px">Total Returns</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.4rem;color:#00D084">₹{profit:,.0f}</div>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:18px;padding:16px;text-align:center;border:1px solid rgba(255,255,255,0.1)">
          <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;letter-spacing:1px;color:#555;margin-bottom:8px">Return Rate</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.4rem;color:#FF6B35">{profit/invested*100:.1f}%</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:8px'>📋 Report Includes</div>", unsafe_allow_html=True)
    ic = st.columns(4)
    for col, (icon, bg, lbl, desc) in zip(ic, [
        ("👤","#FFFBCC","User Profile","Name, age, streak, XP"),
        ("💼","#E8F7FF","Financial Profile","Allowance, risk, goals"),
        ("📈","#E6FFF5","Projections","Year-by-year breakdown"),
        ("🏅","#F0EBFF","Achievements","Badges and points"),
    ]):
        col.markdown(f"""
        <div style="background:{bg};border-radius:20px;padding:18px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.06)">
          <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
          <div style="font-weight:900;font-size:0.82rem;color:#141414;margin-bottom:4px">{lbl}</div>
          <div style="font-size:0.72rem;color:#6B6B6B;font-weight:700">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("📥  Generate and Download PDF", type="primary"):
        with st.spinner("Building your report... ✨"):
            pdf = generate_pdf(user, profile, gami, streak)
        if pdf:
            st.download_button("⬇️  Download PDF Report", data=pdf,
                file_name=f"SmartSIP_{user['username']}.pdf",
                mime="application/pdf", type="primary")
            st.success("🎉 Your report is ready!")
        else:
            st.error("PDF generation failed. Check that ReportLab is installed.")
