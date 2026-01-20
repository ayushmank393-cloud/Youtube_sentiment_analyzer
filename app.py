import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper import get_comments
from model import clean_text, analyze_sentiment

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="YouTube Sentiment Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f4f6fb;
}

.hero {
    padding: 40px;
    border-radius: 24px;
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
    margin-bottom: 30px;
    text-align: center;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(8px);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

.kpi {
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-weight: 700;
}

.kpi-positive { background: linear-gradient(135deg, #11998e, #38ef7d); }
.kpi-neutral  { background: linear-gradient(135deg, #757F9A, #D7DDE8); color: #222; }
.kpi-negative { background: linear-gradient(135deg, #cb2d3e, #ef473a); }

.kpi h2 {
    font-size: 36px;
    margin: 0;
}

.kpi p {
    margin-top: 6px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
    font-size: 14px;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown('<div class="sidebar-title">🎥 YouTube Analyzer</div>', unsafe_allow_html=True)
st.sidebar.markdown("Analyze audience emotions using **AI-powered NLP**")
st.sidebar.markdown("---")

video_url = st.sidebar.text_input("🔗 YouTube Video URL")
max_comments = st.sidebar.slider("💬 Number of Comments", 20, 200, 100)
analyze_btn = st.sidebar.button("🚀 Analyze Now")

# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
    <h1>📊 YouTube Sentiment Analyzer</h1>
    <p>Understand how people really feel about a video using Natural Language Processing</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Analysis ----------------
if analyze_btn:
    if video_url.strip() == "":
        st.error("❌ Please enter a valid YouTube URL")
    else:
        with st.spinner("🔍 Fetching comments & analyzing sentiment..."):
            comments = get_comments(video_url, max_comments)

            results = {"Positive": 0, "Neutral": 0, "Negative": 0}
            categorized_comments = {"Positive": [], "Neutral": [], "Negative": []}
            data = []

            for comment in comments:
                cleaned = clean_text(comment)
                sentiment = analyze_sentiment(cleaned)
                results[sentiment] += 1
                categorized_comments[sentiment].append(comment)
                data.append({"Comment": comment, "Sentiment": sentiment})

        st.success("✅ Analysis Completed Successfully")

        # ---------------- KPI CARDS ----------------
        c1, c2, c3 = st.columns(3)

        c1.markdown(f"""
        <div class="kpi kpi-positive">
            <h2>😊 {results['Positive']}</h2>
            <p>Positive</p>
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="kpi kpi-neutral">
            <h2>😐 {results['Neutral']}</h2>
            <p>Neutral</p>
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="kpi kpi-negative">
            <h2>😠 {results['Negative']}</h2>
            <p>Negative</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------- Insight ----------------
        overall = max(results, key=results.get)
        st.info(f"📌 **Overall Audience Sentiment:** {overall}")

        # ---------------- Charts ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Sentiment Distribution</div>', unsafe_allow_html=True)

        sentiment_df = pd.DataFrame({
            "Sentiment": results.keys(),
            "Count": results.values()
        })

        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots(figsize=(4.8, 4))
            ax1.bar(sentiment_df["Sentiment"], sentiment_df["Count"])
            ax1.set_title("Bar Chart")
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4.8, 4))
            ax2.pie(
                sentiment_df["Count"],
                labels=sentiment_df["Sentiment"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax2.axis("equal")
            st.pyplot(fig2)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- Comments ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💬 Sample Comments</div>', unsafe_allow_html=True)

        t1, t2, t3 = st.tabs(["😊 Positive", "😐 Neutral", "😠 Negative"])

        with t1:
            for c in categorized_comments["Positive"][:5]:
                st.success(c)

        with t2:
            for c in categorized_comments["Neutral"][:5]:
                st.info(c)

        with t3:
            for c in categorized_comments["Negative"][:5]:
                st.error(c)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- Download ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⬇️ Download Results</div>', unsafe_allow_html=True)

        df = pd.DataFrame(data)
        st.download_button(
            "Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "youtube_sentiment_results.csv",
            "text/csv"
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built with ❤️ using <b>Python • NLP • Streamlit</b><br>
Portfolio-ready Sentiment Analysis Dashboard
</div>
""", unsafe_allow_html=True)
