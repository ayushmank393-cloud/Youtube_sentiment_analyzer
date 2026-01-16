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
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    margin-bottom: 30px;
    text-align: center;
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

.kpi {
    text-align: center;
    padding: 20px;
    border-radius: 16px;
    background: #f9fafc;
    box-shadow: inset 0 0 0 1px #eee;
}

.kpi h2 {
    font-size: 34px;
    margin: 0;
}

.kpi p {
    margin: 5px 0 0;
    font-weight: 600;
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

# ---------------- Hero Header (CENTERED) ----------------
st.markdown("""
<div class="hero">
    <h1>📊 YouTube Sentiment Analyzer</h1>
    <p>Understand how people really feel about a video using Natural Language Processing.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Analysis ----------------
if analyze_btn:
    if video_url.strip() == "":
        st.error("❌ Please enter a valid YouTube URL")
    else:
        progress = st.progress(0)
        with st.spinner("🔍 Fetching comments & analyzing sentiment..."):
            comments = get_comments(video_url, max_comments)

            results = {"Positive": 0, "Neutral": 0, "Negative": 0}
            categorized_comments = {"Positive": [], "Neutral": [], "Negative": []}
            data = []

            for i, comment in enumerate(comments):
                cleaned = clean_text(comment)
                sentiment = analyze_sentiment(cleaned)

                results[sentiment] += 1
                categorized_comments[sentiment].append(comment)
                data.append({"Comment": comment, "Sentiment": sentiment})

                progress.progress((i + 1) / len(comments))

        st.success("✅ Analysis Completed Successfully")

        # ---------------- KPI CARDS ----------------
        c1, c2, c3 = st.columns(3)

        c1.markdown(f"""
        <div class="kpi">
            <h2>😊 {results['Positive']}</h2>
            <p>Positive</p>
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="kpi">
            <h2>😐 {results['Neutral']}</h2>
            <p>Neutral</p>
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="kpi">
            <h2>😠 {results['Negative']}</h2>
            <p>Negative</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------- Overall Verdict ----------------
        overall = max(results, key=results.get)
        verdict = {
            "Positive": "🎉 Overall audience sentiment is **Positive**",
            "Neutral": "🙂 Overall audience sentiment is **Neutral**",
            "Negative": "⚠️ Overall audience sentiment is **Negative**"
        }
        st.info(verdict[overall])

        # ---------------- Visualization ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Sentiment Visualization</div>', unsafe_allow_html=True)

        sentiment_df = pd.DataFrame({
            "Sentiment": results.keys(),
            "Count": results.values()
        })

        col1, col2 = st.columns(2)

        with col1:
            fig_bar, ax = plt.subplots(figsize=(4.5, 3.5))
            ax.bar(sentiment_df["Sentiment"], sentiment_df["Count"])
            ax.set_title("Sentiment Count")
            st.pyplot(fig_bar)

        with col2:
            fig_pie, ax2 = plt.subplots(figsize=(4.5, 3.5))
            ax2.pie(
                sentiment_df["Count"],
                labels=sentiment_df["Sentiment"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax2.axis("equal")
            st.pyplot(fig_pie)

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
            "📥 Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "youtube_sentiment_results.csv",
            "text/csv"
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built with ❤️ using <b>Python • NLP • Streamlit</b><br>
Designed for real-world sentiment insights
</div>
""", unsafe_allow_html=True)
