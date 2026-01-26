import os
import re
import tempfile

import feedparser
import requests
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


def fetch_channel_id(url: str) -> str:
    html = requests.get(url, timeout=10).text

    match = re.search(r"channel/(UC[\w-]+)", html)

    if not match:
        raise Exception("Channel ID not found")

    return match.group(1)


def fetch_last_video_id(channel_id: str):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)

    last_video = feed.entries[0]

    return last_video.get("yt_videoid")


def fetch_channel_info(channel_url: str) -> dict:
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    return {
        "custom_id": info.get("id"),
        "name": info.get("channel"),
        "subscribe": info.get("channel_follower_count"),
        "thumbnail": info.get("thumbnails", [{}])[0].get("url"),
        "avatar": info.get("thumbnails", [{}])[-1].get("url"),
        "url": info.get("channel_url"),
        "custom_url": info.get("uploader_url"),
        "last_video": info.get("entries", [{}])[0].get("entries", [{}])[0].get("url"),
    }
