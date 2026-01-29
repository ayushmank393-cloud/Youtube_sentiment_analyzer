import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scraper import get_comments
from model import clean_text, analyze_sentiment
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# ---------------- NLTK Setup ----------------
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

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
.hero h1 { font-size: 46px; font-weight: 800; }
.hero p { font-size: 18px; opacity: 0.9; }

.kpi {
    padding: 22px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-weight: 700;
}
.kpi-positive { background: linear-gradient(135deg, #11998e, #38ef7d); }
.kpi-neutral { background: linear-gradient(135deg, #757F9A, #D7DDE8); color:#222; }
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
    <p>Analyze audience emotions using NLP & Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Analysis ----------------
if analyze_btn:

    if not video_url.strip():
        st.error("❌ Please enter a valid YouTube URL")
        st.stop()

    with st.spinner("🔍 Fetching comments & analyzing sentiment..."):
        comments = get_comments(video_url, max_comments)

    if not comments:
        st.warning("⚠️ No comments found or comments are disabled.")
        st.stop()

    results = {"Positive": 0, "Neutral": 0, "Negative": 0}
    categorized_comments = {"Positive": [], "Neutral": [], "Negative": []}
    data = []
    all_words = []

    progress = st.progress(0)

    for i, comment in enumerate(comments):
        cleaned = clean_text(comment)
        sentiment = analyze_sentiment(cleaned)

        results[sentiment] += 1
        categorized_comments[sentiment].append(comment)
        data.append({"Comment": comment, "Sentiment": sentiment})

        tokens = [
            w for w in word_tokenize(cleaned)
            if w.isalpha() and w.lower() not in stop_words
        ]
        all_words.extend(tokens)

        progress.progress((i + 1) / len(comments))

    total = sum(results.values())

    if total == 0:
        st.error("No analyzable comments found.")
        st.stop()

    st.success(f"✅ Analysis Completed | Total Comments: {total}")

    # ---------------- KPI Section ----------------
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

    # ---------------- Charts ----------------
    st.markdown("### 📊 Sentiment Distribution")

    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(
        results.values(),
        labels=results.keys(),
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.4}
    )
    ax1.set_title("Sentiment Donut Chart")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.bar(results.keys(), results.values())
    ax2.set_title("Sentiment Count")
    st.pyplot(fig2)

    # ---------------- Top Keywords ----------------
    st.markdown("### 🔑 Top Keywords")
    common_words = Counter(all_words).most_common(10)
    st.dataframe(
        pd.DataFrame(common_words, columns=["Word", "Frequency"]),
        use_container_width=True
    )

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
YouTube Sentiment Analysis Project
</div>
""", unsafe_allow_html=True)
