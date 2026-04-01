import streamlit as st
from utils.chatbot import get_response
from utils.gamification import add_points

QUICK_TOPICS = [
    ("💡", "#FFFBCC", "#7A6000", "What is SIP?"),
    ("📈", "#E8F7FF", "#004F80", "Why invest early?"),
    ("⚖️", "#FFE8F5", "#900030", "What is risk?"),
    ("🌐", "#E6FFF5", "#006040", "Diversification?"),
    ("💰", "#F0EBFF", "#4C1D95", "How mutual funds work?"),
    ("✨", "#FFF0EB", "#9A3412", "Power of compounding?"),
]

def show_advisor():
    uid = st.session_state.user["id"]

    # ── Scoped CSS — chat UI only, no HTML in chat bubbles ──────────────────
    st.markdown("""
    <style>
    /* Chat message cards */
    [data-testid="stChatMessage"] {
        background: white !important;
        border-radius: 20px !important;
        padding: 14px 18px !important;
        margin: 6px 0 !important;
        box-shadow: 0 2px 14px rgba(0,0,0,0.06) !important;
        border: 1.5px solid #F0F0F0 !important;
    }
    /* User bubble — yellow tint */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #FFFDE8 !important;
        border-color: #F0E800 !important;
    }
    /* Message text */
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li,
    [data-testid="stChatMessageContent"] span {
        font-family: 'Nunito Sans', sans-serif !important;
        font-size: 0.92rem !important;
        line-height: 1.7 !important;
        color: #222222 !important;
    }
    [data-testid="stChatMessageContent"] strong {
        font-family: 'Nunito', sans-serif !important;
        font-weight: 900 !important;
        color: #141414 !important;
    }
    /* Avatars */
    [data-testid="chatAvatarIcon-assistant"] {
        background: #FFFC00 !important;
        color: #141414 !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
    }
    [data-testid="chatAvatarIcon-user"] {
        background: #141414 !important;
        color: #FFFC00 !important;
        border-radius: 50% !important;
    }
    /* Chat input box */
    [data-testid="stChatInputTextArea"] textarea {
        background: white !important;
        border: 2px solid #E8E8E8 !important;
        border-radius: 16px !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        color: #141414 !important;
        padding: 12px 16px !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    [data-testid="stChatInputTextArea"]:focus-within textarea {
        border-color: #FFFC00 !important;
        box-shadow: 0 0 0 4px rgba(255,252,0,0.18) !important;
        outline: none !important;
    }
    /* Submit button */
    [data-testid="stChatInputSubmitButton"] button {
        background: #FFFC00 !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 3px 0 #D4D000 !important;
        transition: transform 0.15s, box-shadow 0.15s !important;
    }
    [data-testid="stChatInputSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 0 #D4D000 !important;
    }
    /* Quick topic buttons — override global yellow for these */
    [data-testid="stHorizontalBlock"] .stButton > button {
        background: #F2F2F2 !important;
        color: #141414 !important;
        box-shadow: 0 2px 0 #DEDEDE !important;
        font-size: 0.8rem !important;
        padding: 8px 12px !important;
    }
    [data-testid="stHorizontalBlock"] .stButton > button:hover {
        background: #FFFC00 !important;
        box-shadow: 0 3px 0 #D4D000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Page header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:24px 0 24px 0">
      <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:6px">CONVERSATIONAL AI</div>
      <div style="font-family:'Nunito',sans-serif;font-weight:900;font-size:2rem;color:#141414;margin-bottom:6px">AI Financial Advisor</div>
      <div style="font-size:0.88rem;color:#6B6B6B;font-weight:600">Ask anything about investing and earn <strong style="color:#141414">+5 points</strong> per question</div>
    </div>""", unsafe_allow_html=True)

    # ── Quick topic chips (native Streamlit buttons only) ────────────────────
    st.markdown("""
    <div style="font-size:0.68rem;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#9B9B9B;margin-bottom:10px">Quick Topics</div>
    """, unsafe_allow_html=True)

    cols = st.columns(6)
    for i, (icon, bg, tc, question) in enumerate(QUICK_TOPICS):
        with cols[i]:
            if st.button(f"{icon}  {question.replace('?','')}", key=f"qt_{i}", use_container_width=True):
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"role":"user","title":question,"content":""})
                title, content = get_response(question)
                st.session_state.chat_history.append({"role":"bot","title":title,"content":content})
                add_points(uid, 5, "chat")
                st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Initialize chat ───────────────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "bot",
                "title": "Hey there! 👋",
                "content": "I'm your SmartSIP advisor. Ask me about **SIP**, **mutual funds**, **risk**, **compounding**, **diversification**, or **inflation**. Every question earns you **+5 points**!"
            }
        ]

    # ── Render chat using ONLY native st.chat_message — zero HTML ────────────
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"**{msg['title']}**")
        else:
            with st.chat_message("assistant", avatar="💛"):
                st.markdown(f"**{msg['title']}**")
                if msg.get("content"):
                    st.markdown(msg["content"])

    # ── Native chat input — no HTML at all ───────────────────────────────────
    user_input = st.chat_input("Ask about SIP, risk, mutual funds, compounding...")
    if user_input:
        st.session_state.chat_history.append({"role":"user","title":user_input,"content":""})
        title, content = get_response(user_input)
        st.session_state.chat_history.append({"role":"bot","title":title,"content":content})
        add_points(uid, 5, "chat")
        st.rerun()

    # ── Topics reference card (pure HTML, no dynamic data — safe) ────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    topics_pills = "".join([
        f'<span style="background:{bg};color:{tc};font-size:0.75rem;font-weight:800;padding:5px 14px;border-radius:999px;margin:3px 2px;display:inline-block">{icon} {q.replace("?","")}</span>'
        for icon, bg, tc, q in QUICK_TOPICS
    ])
    st.markdown(f"""
    <div style="background:#F9F9F9;border-radius:20px;padding:18px 22px;border:1.5px solid #EEEEEE">
      <div style="font-size:0.7rem;font-weight:900;text-transform:uppercase;letter-spacing:1.5px;color:#AAAAAA;margin-bottom:12px">Topics I can help with</div>
      <div style="line-height:2.4">{topics_pills}</div>
    </div>""", unsafe_allow_html=True)
