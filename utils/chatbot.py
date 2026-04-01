RESPONSES = {
    "sip": (
        "💡 What is SIP?",
        "A Systematic Investment Plan (SIP) lets you invest a fixed amount every month in mutual funds. It is like a monthly savings habit that grows your wealth over time through the power of compounding!"
    ),
    "invest early": (
        "🚀 Why Invest Early?",
        "Starting early gives your money more time to compound. If you invest ₹500/month at age 15 vs 25, you could end up with 3x more wealth by age 40 — just because of those extra 10 years!"
    ),
    "risk": (
        "⚖️ What is Risk?",
        "Investment risk is the chance that your investment may lose value. Higher risk means higher potential returns. As a teen, you have time to recover from losses, so you can afford moderate risk."
    ),
    "diversification": (
        "🌐 What is Diversification?",
        "Diversification means spreading your money across different types of investments like stocks, bonds, and gold. If one falls, others may rise — reducing your overall loss."
    ),
    "mutual fund": (
        "📊 How Mutual Funds Work",
        "A mutual fund pools money from thousands of investors. A professional fund manager invests this in stocks, bonds, etc. You get units proportional to your investment and share in profits and losses."
    ),
    "compounding": (
        "✨ Power of Compounding",
        "Compounding means you earn returns on your previous returns! ₹1000 at 12% becomes ₹1120 in year 1, then ₹1254 in year 2 — it snowballs massively over time!"
    ),
    "inflation": (
        "📈 Inflation and Investing",
        "Inflation slowly reduces your money's buying power — prices rise around 6% every year in India. If your savings earn less than inflation, you are actually losing money. Investing helps you beat inflation."
    ),
    "goal": (
        "🎯 Goal-Based Investing",
        "Set clear financial goals like buying a laptop in 2 years or funding college in 5 years. Then choose investments that match your timeline and risk appetite for each specific goal."
    ),
}

def get_response(user_input):
    user_input = user_input.lower()
    for keyword, (title, content) in RESPONSES.items():
        if keyword in user_input:
            return title, content
    return (
        "🤖 Smart SIP Advisor",
        "I can help with: SIP, investing early, risk, diversification, mutual funds, compounding, inflation, or goal-based investing. Try asking about any of these topics!"
    )
