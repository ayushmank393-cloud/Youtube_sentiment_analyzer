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
.main-title {
    font-size: 42px;
    font-weight: 700;
}
.subtitle {
    font-size: 18px;
    color: #555;
}
.yellow-line {
    width: 120px;
    height: 4px;
    background-color: #FFD700;
    margin: 10px 0 25px 0;
}
.metric-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8f9fa;
    text-align: center;
}
.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown("## 🎥 YouTube Analyzer")
st.sidebar.markdown("Analyze audience sentiment using **NLP**")
st.sidebar.markdown("---")

video_url = st.sidebar.text_input("🔗 YouTube Video URL")
max_comments = st.sidebar.slider("💬 Number of comments", 20, 200, 100)
analyze_btn = st.sidebar.button("🚀 Analyze Sentiment")

# ---------------- Hero Section ----------------
st.markdown('<div class="main-title">📊 YouTube Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="yellow-line"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Understand what people really think by analyzing YouTube comments using Natural Language Processing.</div>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- Analysis ----------------
if analyze_btn:
    if video_url.strip() == "":
        st.error("❌ Please enter a valid YouTube URL")
    else:
        with st.spinner("🔍 Fetching comments and analyzing sentiment..."):
            comments = get_comments(video_url, max_comments)

            results = {"Positive": 0, "Neutral": 0, "Negative": 0}
            categorized_comments = {
                "Positive": [],
                "Neutral": [],
                "Negative": []
            }
            data = []

            for comment in comments:
                cleaned = clean_text(comment)
                sentiment = analyze_sentiment(cleaned)

                results[sentiment] += 1
                categorized_comments[sentiment].append(comment)

                data.append({
                    "Comment": comment,
                    "Sentiment": sentiment
                })

        st.success("✅ Analysis Completed Successfully")

        # ---------------- Metrics ----------------
        st.markdown("## 📈 Sentiment Overview")
        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <h2>😊</h2>
                <h3>{results['Positive']}</h3>
                <p>Positive</p>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <h2>😐</h2>
                <h3>{results['Neutral']}</h3>
                <p>Neutral</p>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-box">
                <h2>😠</h2>
                <h3>{results['Negative']}</h3>
                <p>Negative</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- Pie Chart ----------------
        st.markdown("## 🥧 Sentiment Distribution")

        fig, ax = plt.subplots()
        ax.pie(
            results.values(),
            labels=results.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

        # ---------------- Comments ----------------
        st.markdown("## 💬 Sample Comments")
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

        # ---------------- Download ----------------
        st.markdown("## ⬇️ Download Results")
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV",
            csv,
            "youtube_sentiment_results.csv",
            "text/csv"
        )

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built with ❤️ using <b>Python, NLP & Streamlit</b>
</div>
""", unsafe_allow_html=True)
