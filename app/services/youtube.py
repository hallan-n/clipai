import os
import tempfile
import feedparser
from yt_dlp import YoutubeDL
from datetime import datetime


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


def fetch_video_infos(channel_id: str, limit: int) -> list[dict]:
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

        video["tags"] = [tag["term"] for tag in entry.tags] if hasattr(entry, "tags") else []

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
        "custom_id": info.get("uploader_url").split("/")[-1] or info.get("id"),
        "name": info.get("channel"),
        "subscribe": info.get("channel_follower_count"),
        "thumbnail": thumbnails[0].get("url") if len(thumbnails) > 0 else "",
        "avatar": thumbnails[-1].get("url") if thumbnails else "",
        "url": info.get("channel_url"),
        "custom_url": info.get("uploader_url"),
        "last_video": (
            info.get("entries")[0].get("entries")[0].get("url")
            if len(info.get("entries")) > 0
            else ""
        ),
    }
