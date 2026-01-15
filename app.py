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
    background-color: #f6f7fb;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: white;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    margin-bottom: 25px;
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

.highlight {
    color: #1f4037;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown('<div class="sidebar-title">🎥 YouTube Analyzer</div>', unsafe_allow_html=True)
st.sidebar.markdown("Understand audience emotions using **AI-powered NLP**")
st.sidebar.markdown("---")

video_url = st.sidebar.text_input("🔗 YouTube Video URL")
max_comments = st.sidebar.slider("💬 Number of Comments", 20, 200, 100)
analyze_btn = st.sidebar.button("🚀 Analyze Now")

# ---------------- Hero Header ----------------
st.markdown("""
<div class="hero">
    <h1>📊 YouTube Sentiment Analyzer</h1>
    <p>Analyze <b>Positive</b>, <b>Neutral</b>, and <b>Negative</b> emotions from YouTube comments using Natural Language Processing.</p>
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

                data.append({
                    "Comment": comment,
                    "Sentiment": sentiment
                })

        st.success("✅ Analysis Completed Successfully")

        # ---------------- Visualization Card ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Sentiment Visualization</div>', unsafe_allow_html=True)

        sentiment_df = pd.DataFrame({
            "Sentiment": list(results.keys()),
            "Count": list(results.values())
        })

        col1, col2 = st.columns(2)

        with col1:
            fig_bar, ax_bar = plt.subplots(figsize=(4.5, 3.5))
            ax_bar.bar(sentiment_df["Sentiment"], sentiment_df["Count"])
            ax_bar.set_title("Sentiment Count")
            ax_bar.set_xlabel("Sentiment")
            ax_bar.set_ylabel("Count")
            st.pyplot(fig_bar)

        with col2:
            fig_pie, ax_pie = plt.subplots(figsize=(4.5, 3.5))
            ax_pie.pie(
                sentiment_df["Count"],
                labels=sentiment_df["Sentiment"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax_pie.set_title("Sentiment Distribution")
            ax_pie.axis("equal")
            st.pyplot(fig_pie)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- Table Card ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Sentiment Summary</div>', unsafe_allow_html=True)
        st.dataframe(sentiment_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- Comments Card ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💬 Sample Comments</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["😊 Positive", "😐 Neutral", "😠 Negative"])

        with tab1:
            for c in categorized_comments["Positive"][:5]:
                st.success(c)

        with tab2:
            for c in categorized_comments["Neutral"][:5]:
                st.info(c)

        with tab3:
            for c in categorized_comments["Negative"][:5]:
                st.error(c)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- Download ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⬇️ Download Results</div>', unsafe_allow_html=True)

        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="youtube_sentiment_results.csv",
            mime="text/csv"
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built with ❤️ using <b>Python • NLP • Streamlit</b><br>
Made for real-world sentiment insights
</div>
""", unsafe_allow_html=True)
