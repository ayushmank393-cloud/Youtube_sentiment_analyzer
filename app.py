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
    font-size: 40px;
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
.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown("## 🎥 YouTube Sentiment Analyzer")
st.sidebar.markdown("Analyze YouTube comments using **NLP**")
st.sidebar.markdown("---")

video_url = st.sidebar.text_input("🔗 Enter YouTube Video URL")
max_comments = st.sidebar.slider("💬 Number of Comments", 20, 200, 100)
analyze_btn = st.sidebar.button("🚀 Analyze Sentiment")

# ---------------- Header ----------------
st.markdown('<div class="main-title">📊 YouTube Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="yellow-line"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">This application analyzes YouTube comments for Positive, Neutral, and Negative sentiment.</div>',
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

        # ---------------- Charts ----------------
        st.markdown("## 📊 Sentiment Visualization")

        sentiment_df = pd.DataFrame({
            "Sentiment": list(results.keys()),
            "Count": list(results.values())
        })

        col1, col2 = st.columns(2)

        # -------- Bar Chart (Smaller) --------
        with col1:
            fig_bar, ax_bar = plt.subplots(figsize=(4, 3))
            ax_bar.bar(
                sentiment_df["Sentiment"],
                sentiment_df["Count"],
                color="#FFD700"
            )
            ax_bar.set_title("Bar Chart")
            ax_bar.set_xlabel("Sentiment")
            ax_bar.set_ylabel("Count")
            st.pyplot(fig_bar)

        # -------- Pie Chart (Smaller) --------
        with col2:
            fig_pie, ax_pie = plt.subplots(figsize=(4, 3))
            ax_pie.pie(
                sentiment_df["Count"],
                labels=sentiment_df["Sentiment"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax_pie.set_title("Pie Chart")
            ax_pie.axis("equal")
            st.pyplot(fig_pie)

        # ---------------- Table ----------------
        st.markdown("## 📋 Sentiment Summary Table")
        st.dataframe(sentiment_df, use_container_width=True)

        # ---------------- Sample Comments ----------------
        st.markdown("## 💬 Sample Comments")

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

        # ---------------- Download CSV ----------------
        st.markdown("## ⬇️ Download Results")

        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="youtube_sentiment_results.csv",
            mime="text/csv"
        )

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built with ❤️ using <b>Python, NLP, and Streamlit</b>
</div>
""", unsafe_allow_html=True)
