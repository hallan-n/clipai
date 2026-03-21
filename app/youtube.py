import os
import pickle
import re
from datetime import datetime

import feedparser
import requests
from consts import (
    YOUTUBE_API_CLIENT_SECRET_FILE,
    YOUTUBE_API_SCOPES,
    YOUTUBE_API_TOKEN_FILE,
)
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from models import YouTubeVideo
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL


def fetch_transcribe(video_url: str):
    video_id = video_url.split("?v=")[-1]
    try:
        segments = YouTubeTranscriptApi().fetch(video_id, languages=["pt", "pt-BR"])

        result = []

        for s in segments:
            start = float(s.start)
            duration = float(s.duration)
            end = start + duration

            result.append(
                {
                    "text": s.text,
                    "start": start,
                    "end": end,
                }
            )

        return result
    except:
        return None


def fetch_video_info(video_url: str) -> dict:
    ydl_opts = {"skip_download": True, "quiet": True, "extract_flat": True}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    return {
        "video_id": info.get("id"),
        "url": info.get("webpage_url"),
        "channel_url": info.get("channel_url"),
        "title": info.get("title"),
        "description": info.get("description"),
        "published_at": info.get("upload_date"),
        "duration": info.get("duration"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "channel_id": info.get("channel_id"),
        "channel_title": info.get("uploader"),
        "thumbnail": info.get("thumbnail"),
        "heatmap": info.get("heatmap"),
        "resolutions": info.get("resolution"),
        "is_live": info.get("is_live", False) or info.get("was_live", False),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "tags": ",".join(info.get("tags")) if info.get("tags") else "",
        "categories": (
            ",".join(info.get("categories")) if info.get("categories") else ""
        ),
    }


def download_video(video_url: str, output_path: str) -> str:

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return output_path


def fetch_video_infos(channel_url: str, limit: int = 15) -> list[dict]:
    html = requests.get(channel_url).text
    regex = r"(https:\/\/www\.youtube\.com\/channel\/)(\w+)"
    channel_id = re.search(regex, html).group(2)

    limit = limit if (limit > 0 and limit <= 15) else 15
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)

    videos: list[dict] = []

    for entry in feed.entries[:limit]:
        video: dict = {}

        video["video_id"] = entry.get("yt_videoid")
        video["url"] = entry.get("link")
        video["title"] = entry.get("title")

        video["description"] = entry.get("summary")

        if hasattr(entry, "published_parsed"):
            video["published_at"] = datetime(*entry.published_parsed[:6]).isoformat()
        else:
            video["published_at"] = None

        if hasattr(entry, "updated_parsed"):
            video["updated_at"] = datetime(*entry.updated_parsed[:6]).isoformat()
        else:
            video["updated_at"] = None

        video["author"] = entry.author if hasattr(entry, "author") else None

        thumbnail = None
        if "media_thumbnail" in entry and entry.media_thumbnail:
            thumbnail = entry.media_thumbnail[0].get("url")
        video["thumbnail"] = thumbnail

        duration = None
        if "media_content" in entry and entry.media_content:
            duration = entry.media_content[0].get("duration")
            if duration:
                duration = int(duration)
        video["duration"] = duration

        video["tags"] = (
            [tag["term"] for tag in entry.tags] if hasattr(entry, "tags") else []
        )

        videos.append(video)

    return videos


def fetch_channel_info(channel_url: str) -> dict:
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    thumbnails = info.get("thumbnails") or []

    return {
        "custom_id": (
            info.get("uploader_url", "").split("/")[-1]
            if info.get("uploader_url", "")
            else info.get("id")
        ),
        "name": info.get("channel"),
        "subscribe": info.get("channel_follower_count"),
        "thumbnail": thumbnails[0].get("url") if len(thumbnails) > 0 else "",
        "avatar": thumbnails[-1].get("url") if thumbnails else "",
        "url": info.get("channel_url"),
        "custom_url": info.get("uploader_url"),
        "last_video": info.get("entries", [{}])[0].get("url", ""),
    }


def _get_credentials():
    creds = None

    if os.path.exists(YOUTUBE_API_TOKEN_FILE):
        with open(YOUTUBE_API_TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_API_CLIENT_SECRET_FILE, YOUTUBE_API_SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(YOUTUBE_API_TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return creds


def upload_video(video: YouTubeVideo):
    creds = _get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video.title,
                "description": video.description,
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": video.published_at,
            },
        },
        media_body=MediaFileUpload(video.video_path),
    )
    response = request.execute()
    video.video_id = response["id"]
    video.channel_id = response["snippet"]["channelId"]

    if video.thumb_path:
        youtube.thumbnails().set(
            videoId=video.video_id, media_body=MediaFileUpload(video.thumb_path)
        ).execute()

    return video


"""
#cortesmbl #partidomissao #mbl
👉 Quer saber mais? Acompanhe as lives do MBL, de segunda à sexta-feira no canal:    / @mblivetv  

👀 Vídeo original:    • URGENTE: VORCARO VAI DELATAR ATÉ O STF | A...  

Se gostou do vídeo, não se esqueça de deixar o like e se inscrever no canal 💪

Até a próxima e fique com Deus 🙏

#cortesmbl #partidomissao #mbl #renansantos #mamaefalei #kimkataguiri
"""
