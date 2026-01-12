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

# ---------------- Sidebar ----------------
st.sidebar.title("🎥 YouTube Sentiment Analyzer")
st.sidebar.write("Analyze sentiment of YouTube comments")

video_url = st.sidebar.text_input("🔗 Enter YouTube Video URL")
max_comments = st.sidebar.slider("💬 Number of Comments", 20, 200, 100)
analyze_btn = st.sidebar.button("🚀 Analyze")

# ---------------- Main UI ----------------
st.title("📊 YouTube Sentiment Analyzer")
st.write("This app analyzes **Positive, Neutral, and Negative** sentiment from YouTube comments using NLP.")

if analyze_btn:
    if video_url.strip() == "":
        st.error("❌ Please enter a valid YouTube URL")
    else:
        with st.spinner("Fetching comments and analyzing sentiment..."):
            comments = get_comments(video_url, max_comments)

            results = {"Positive": 0, "Neutral": 0, "Negative": 0}
            categorized_comments = {
                "Positive": [],
                "Neutral": [],
                "Negative": []
            }

            data = []  # for CSV

            for comment in comments:
                cleaned = clean_text(comment)
                sentiment = analyze_sentiment(cleaned)

                results[sentiment] += 1
                categorized_comments[sentiment].append(comment)

                data.append({
                    "Comment": comment,
                    "Sentiment": sentiment
                })

        st.success("✅ Analysis Complete")

        # ----------- Metrics -----------
        col1, col2, col3 = st.columns(3)
        col1.metric("😊 Positive", results["Positive"])
        col2.metric("😐 Neutral", results["Neutral"])
        col3.metric("😠 Negative", results["Negative"])

        # ----------- Pie Chart -----------
        st.subheader("📊 Sentiment Distribution")
        fig, ax = plt.subplots()
        ax.pie(
            results.values(),
            labels=results.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

        # ----------- Sample Comments -----------
        st.subheader("💬 Sample Comments")

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

        # ----------- Download CSV -----------
        st.subheader("⬇️ Download Results")
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="youtube_sentiment_results.csv",
            mime="text/csv"
        )

st.markdown("---")
st.markdown("Built with ❤️ using **Python, NLP, and Streamlit**")
