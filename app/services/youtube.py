import os
import re
import tempfile

import feedparser
import requests
from services.logger import logger
from yt_dlp import YoutubeDL


def fetch_video_info(video_url: str) -> dict:
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    return {
        "video_id": info.get("id"),
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
    }


def download_video_temp(video_url: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="video_")
    output = os.path.join(temp_dir, "video.%(ext)s")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output,
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return os.path.join(temp_dir, "video.mp4")


def get_channel_id(url: str) -> str:
    username = url.split("@")[1]
    url = f"https://www.youtube.com/{username}"
    html = requests.get(url, timeout=10).text

    match = re.search(r"channel/(UC[\w-]+)", html)

    if not match:
        raise Exception("Channel ID not found")

    return match.group(1)


def get_last_video_id(channel_id: str):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)

    last_video = feed.entries[0]

    return last_video.get("yt_videoid")
