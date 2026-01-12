from googleapiclient.discovery import build

# 🔴 REPLACE WITH YOUR API KEY
API_KEY = "AIzaSyASYZNUEEE-B2gblS9N6tpyz6vWKKg2uP8"

youtube = build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1][:11]
    return url[-11:]

def get_comments(video_url, max_results=100):
    video_id = extract_video_id(video_url)
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )

    response = request.execute()

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments
