import streamlit as st
import pandas as pd
from utils.gamification import complete_lesson, get_gamification

DIFF = {
    "Beginner":     {"color":"#00D084","bg":"#E6FFF5","border":"#00D084","icon":"🌱","label_bg":"#E6FFF5"},
    "Intermediate": {"color":"#FF6B35","bg":"#FFF0EB","border":"#FF6B35","icon":"📈","label_bg":"#FFF0EB"},
    "Advanced":     {"color":"#8B5CF6","bg":"#F0EBFF","border":"#8B5CF6","icon":"🚀","label_bg":"#F0EBFF"},
}

def show_education():
    uid        = st.session_state.user["id"]
    lessons_df = pd.read_csv("data/financial_lessons.csv")
    gami       = get_gamification(uid)
    completed  = gami["lessons"]
    total      = len(lessons_df)
    done       = len(completed)
    pct        = done / total if total else 0

    st.markdown("""
    <div style="padding:24px 0 20px 0" class="slide-up">
      <div class="section-tag">📚 Learn & Earn</div>
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2rem;color:#141414">
        Financial Education
      </div>
      <div style="font-size:0.88rem;color:#6B6B6B;font-weight:700;margin-top:4px">
        Complete lessons, earn points and unlock badges 🏅
      </div>
    </div>""", unsafe_allow_html=True)

    # Progress banner
    st.markdown(f"""
    <div style="background:#FFFC00;border-radius:24px;padding:20px 24px;margin-bottom:20px;
      box-shadow:0 4px 0 #E6E300">
      <div style="display:flex;align-items:center;gap:20px">
        <div style="font-size:2.5rem">{'🏆' if done==total else '📚'}</div>
        <div style="flex:1">
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1rem;
            color:#141414;margin-bottom:8px">
            {done}/{total} Lessons Completed · {pct*100:.0f}% Done
          </div>
          <div style="background:rgba(0,0,0,0.1);border-radius:999px;height:10px">
            <div style="width:{pct*100:.1f}%;height:100%;background:#141414;
              border-radius:999px;transition:width 0.4s ease"></div>
          </div>
        </div>
        <div style="text-align:center;min-width:56px">
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2rem;
            color:#141414">{pct*100:.0f}%</div>
          <div style="font-size:0.7rem;color:#6B6000;font-weight:900">DONE</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Lesson cards
    for _, row in lessons_df.iterrows():
        title, content, points, diff = row["title"], row["content"], row["points"], row["difficulty"]
        is_done = title in completed
        cfg     = DIFF.get(diff, DIFF["Beginner"])

        with st.expander(f"{cfg['icon']}  {title}  {'✅' if is_done else f'· ⭐ {points} pts'}"):
            cc, ca = st.columns([3,1])
            with cc:
                st.markdown(f"""
                <div style="background:{cfg['bg']};border-left:4px solid {cfg['color']};
                  border-radius:0 16px 16px 0;padding:16px 20px;margin-bottom:8px">
                  <p style="font-size:0.92rem;color:#141414;line-height:1.75;
                    font-weight:600;margin:0">{content}</p>
                </div>""", unsafe_allow_html=True)

            with ca:
                st.markdown(f"""
                <div style="background:{cfg['label_bg']};border-radius:20px;
                  padding:16px;text-align:center;border:3px solid {cfg['color']}">
                  <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;
                    letter-spacing:1px;color:#6B6B6B;margin-bottom:4px">Difficulty</div>
                  <div style="font-size:1.1rem">{cfg['icon']}</div>
                  <div style="font-weight:900;font-size:0.85rem;color:{cfg['color']};
                    margin-bottom:12px">{diff}</div>
                  <div style="font-size:0.65rem;font-weight:900;text-transform:uppercase;
                    letter-spacing:1px;color:#6B6B6B;margin-bottom:4px">Reward</div>
                  <div style="font-family:'Nunito',sans-serif;font-weight:900;
                    font-size:1.3rem;color:#141414">⭐{points}</div>
                </div>""", unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if is_done:
                    st.markdown("""
                    <div style="background:#E6FFF5;border-radius:12px;padding:8px;
                      text-align:center;border:2px solid #00D084;color:#00A854;
                      font-weight:900;font-size:0.82rem">✅ Done!</div>""",
                      unsafe_allow_html=True)
                else:
                    if st.button(f"Complete +{points}pt", key=f"les_{title}",
                                 type="primary", use_container_width=True):
                        awarded, pts = complete_lesson(uid, title, points)
                        if awarded:
                            st.success(f"🎉 +{pts} points earned!")
                            st.rerun()

    if done == total and total > 0:
        st.balloons()
        st.markdown("""
        <div style="background:#FFFC00;border-radius:28px;padding:32px;text-align:center;
          box-shadow:0 6px 0 #E6E300;margin-top:16px">
          <div style="font-size:3rem;margin-bottom:12px">🏆</div>
          <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:1.5rem;
            color:#141414">You're a Financial Mastermind!</div>
          <div style="color:#6B6000;font-weight:700;margin-top:8px">
            All lessons complete! You're unstoppable 🚀
          </div>
        </div>""", unsafe_allow_html=True)
