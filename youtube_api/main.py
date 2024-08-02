import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import isodate

# Define the required scope
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Define paths for credentials and token files
CREDENTIALS_PATH = os.environ.get('CREDENTIALS_PATH')
TOKEN_PATH = os.environ.get('TOKEN_PATH')

def fetch_all_videos(channel_id):
    # Authenticate and construct the service
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    youtube = build('youtube', 'v3', credentials=creds)

    # Fetch the uploads playlist ID
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Fetch all videos in the uploads playlist
    videos = []
    next_page_token = None

    while True:
        playlist_response = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            short_link = f"https://youtu.be/{video_id}"
            upload_date = item['contentDetails']['videoPublishedAt']
            duration_response = youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()
            duration_iso = duration_response['items'][0]['contentDetails']['duration']
            duration = isodate.parse_duration(duration_iso)
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            duration_str = f"{int(hours)} hrs {int(minutes)} mins"
            videos.append({
                'video_id': video_id,
                'title': title,
                'short_link': short_link,
                'duration': duration_str,
                'upload_date': upload_date
            })

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

if __name__ == "__main__":
    channel_id = os.environ.get('YOUTUBE_CHANNEL_ID', '')
    videos = fetch_all_videos(channel_id)
    print(f"Total videos fetched: {len(videos)}")
    for video in videos:
        print(video)
    
    # Save to Excel
    df = pd.DataFrame(videos)
    df.to_excel('youtube_videos.xlsx', index=False)