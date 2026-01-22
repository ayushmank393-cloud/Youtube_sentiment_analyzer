import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scraper import get_comments
from model import clean_text, analyze_sentiment
from nltk.tokenize import word_tokenize

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="YouTube Sentiment Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
.hero {
    padding: 45px;
    border-radius: 26px;
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 { font-size: 48px; font-weight: 800; }
.hero p { font-size: 18px; opacity: 0.9; }

.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

.kpi {
    padding: 22px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-weight: 700;
}

.kpi-positive { background: linear-gradient(135deg, #11998e, #38ef7d); }
.kpi-neutral { background: linear-gradient(135deg, #757F9A, #D7DDE8); color:#222;}
.kpi-negative { background: linear-gradient(135deg, #cb2d3e, #ef473a); }

.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.title("🎥 YouTube Analyzer")
st.sidebar.markdown("---")
video_url = st.sidebar.text_input("🔗 YouTube Video URL")
max_comments = st.sidebar.slider("💬 Number of Comments", 20, 300, 100)
sentiment_filter = st.sidebar.selectbox(
    "🎯 Filter Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)
analyze_btn = st.sidebar.button("🚀 Analyze Now")

# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
    <h1>📊 YouTube Sentiment Analyzer</h1>
    <p>Understand audience emotions using AI-powered Natural Language Processing</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Analysis ----------------
if analyze_btn:
    if not video_url.strip():
        st.error("❌ Please enter a valid YouTube URL")
    else:
        with st.spinner("🔍 Fetching comments & analyzing sentiment..."):
            comments = get_comments(video_url, max_comments)

            results = {"Positive": 0, "Neutral": 0, "Negative": 0}
            categorized_comments = {"Positive": [], "Neutral": [], "Negative": []}
            data = []
            all_words = []

            for comment in comments:
                cleaned = clean_text(comment)
                sentiment = analyze_sentiment(cleaned)

                results[sentiment] += 1
                categorized_comments[sentiment].append(comment)
                data.append({"Comment": comment, "Sentiment": sentiment})

                all_words.extend(word_tokenize(cleaned))

        total = sum(results.values())
        st.success(f"✅ Analysis Completed | Total Comments: {total}")

        # ---------------- KPI ----------------
        c1, c2, c3 = st.columns(3)

        c1.markdown(f"""
        <div class="kpi kpi-positive">
            😊 {results['Positive']}<br>
            {results['Positive']/total*100:.1f}%
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="kpi kpi-neutral">
            😐 {results['Neutral']}<br>
            {results['Neutral']/total*100:.1f}%
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="kpi kpi-negative">
            😠 {results['Negative']}<br>
            {results['Negative']/total*100:.1f}%
        </div>
        """, unsafe_allow_html=True)

        # ---------------- Donut Chart ----------------
        st.markdown("### 📊 Sentiment Distribution")

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            results.values(),
            labels=results.keys(),
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"width": 0.4}
        )
        ax.set_title("Sentiment Donut Chart")
        st.pyplot(fig)

        # ---------------- Top Keywords ----------------
        st.markdown("### 🔑 Top Keywords")
        common_words = Counter(all_words).most_common(10)
        st.write(pd.DataFrame(common_words, columns=["Word", "Frequency"]))

        # ---------------- Comments ----------------
        st.markdown("### 💬 Comments")

        search = st.text_input("🔍 Search comments")

        for sentiment, icon in zip(
            ["Positive", "Neutral", "Negative"], ["😊", "😐", "😠"]
        ):
            if sentiment_filter in ["All", sentiment]:
                with st.expander(f"{icon} {sentiment} Comments"):
                    for c in categorized_comments[sentiment]:
                        if search.lower() in c.lower():
                            st.write("•", c)

        # ---------------- Download ----------------
        df = pd.DataFrame(data)
        st.download_button(
            "⬇️ Download Results (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "youtube_sentiment_results.csv",
            "text/csv"
        )

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built with ❤️ using <b>Python • NLP • Streamlit</b><br>
Enhanced UI + Advanced Features
</div>
""", unsafe_allow_html=True)
