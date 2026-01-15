📊 YouTube Sentiment Analyzer

A Python-based web application that analyzes and visualizes the sentiment of YouTube video comments.
This project demonstrates YouTube API integration, Natural Language Processing (NLP), and interactive data visualization using Streamlit.

🚀 Features

🔗 YouTube API Integration
Fetches real-time comments using YouTube Data API v3

🧠 Sentiment Analysis (NLP)
Classifies comments into Positive, Neutral, and Negative using VADER (NLTK)

📊 Interactive Dashboard
User-friendly interface built with Streamlit

📈 Visualizations
Displays sentiment distribution using bar charts and pie charts

⬇️ CSV Export
Download analyzed comments and sentiment results

🛠️ Tech Stack

Python

Streamlit

YouTube Data API v3

NLTK (VADER Sentiment Analyzer)

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/youtube-sentiment-analyzer.git
cd youtube-sentiment-analyzer

2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Download NLTK VADER Lexicon
import nltk
nltk.download('vader_lexicon')

🔑 YouTube API Setup

Go to Google Cloud Console

Create a new project

Enable YouTube Data API v3

Generate an API key

Set the API key as an environment variable:

set YOUTUBE_API_KEY=your_api_key_here        # Windows
export YOUTUBE_API_KEY=your_api_key_here     # macOS / Linux

▶️ Run the Application
streamlit run app.py


Then open:
http://localhost:8501

Pandas

Matplotlib
