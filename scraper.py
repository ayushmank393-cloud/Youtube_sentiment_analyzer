import os
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from googleapiclient.errors import HttpError

# Load API key securely
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY,
    cache_discovery=False
)

# ---------------- Extract Video ID ----------------
def extract_video_id(url: str):
    try:
        parsed = urlparse(url)

        if parsed.hostname in ("www.youtube.com", "youtube.com"):
            return parse_qs(parsed.query).get("v", [None])[0]

        if parsed.hostname == "youtu.be":
            return parsed.path.lstrip("/")

    except Exception:
        return None

    return None

# ---------------- Get Comments ----------------
def get_comments(video_url: str, max_results: int = 100):
    video_id = extract_video_id(video_url)

    if not video_id:
        return []

    comments = []
    next_page_token = None

    try:
        while len(comments) < max_results:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_results - len(comments)),
                pageToken=next_page_token,
                textFormat="plainText"
            )

            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append(snippet["textDisplay"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    except HttpError as e:
        # Comments disabled / private / quota exceeded
        print("YouTube API Error:", e)
        return []

    except Exception as e:
        print("Unexpected Error:", e)
        return []

    return comments
