📊 YouTube Sentiment Analyzer

A simple Python web app that analyzes the sentiment of YouTube video comments using NLP and Streamlit.

🚀 Features

Fetches comments using YouTube Data API v3
Classifies comments as Positive, Neutral, or Negative
Interactive dashboard with charts
Download results as CSV

🛠️ Tech Stack

Python
Streamlit
NLTK (VADER)
Pandas
Matplotlib

⚙️ How to Run
git clone https://github.com/your-username/youtube-sentiment-analyzer.git
cd youtube-sentiment-analyzer
pip install -r requirements.txt
python -m streamlit run app.py

🔑 API Key

Set your YouTube API key as an environment variable:

Windows
set YOUTUBE_API_KEY=your_api_key_here

macOS / Linux
export YOUTUBE_API_KEY=your_api_key_here
