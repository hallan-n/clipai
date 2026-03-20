from dataclasses import dataclass


@dataclass
class YouTubeVideo:
    video_id: str = None
    channel_id: str = None
    title: str = None
    description: str = None
    tags: list[str] = None
    category_id: str = None
    status: str = None
    thumb_path: str = None
    video_path: str = None
    published_at: str = None
    status: str = None
