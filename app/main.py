import os
from pathlib import Path
from django.urls import include
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application


BASE_DIR = Path(__file__).resolve().parent


settings.configure(
    DEBUG=True,
    SECRET_KEY="dev",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    INTERNAL_IPS=["127.0.0.1"],
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "django_browser_reload",
    ],
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ],
    STATIC_URL="/static/",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
        }
    ],
)


def channels(request):
    return render(request, "channels.html")


def sources(request):
    data = [
        {
            "avatar": "https://yt3.googleusercontent.com/Y1vwq5ulxeRA5JXThkMwmM8_DwJS6fKZpSUkzX9TsMScr3_YcUcB_9HVppFcN_08ewb-3xmrzw=s160-c-k-c0x00ffffff-no-rj",
            "name": "TodeMOTOPodcast",
            "url": "https://www.youtube.com/@TodeMOTOPodcast",
            "fonts": [
                {
                    "name": "TodeMOTOPodcast",
                    "url": "https://www.youtube.com/@TodeMOTOPodcast",
                    "avatar": "https://yt3.googleusercontent.com/Y1vwq5ulxeRA5JXThkMwmM8_DwJS6fKZpSUkzX9TsMScr3_YcUcB_9HVppFcN_08ewb-3xmrzw=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "manualdomundo",
                    "url": "https://www.youtube.com/@manualdomundo",
                    "avatar": "https://yt3.googleusercontent.com/6ZMLayvP5HkX4mgU6ELfDwAl0AWFITQ43mSH7xPcXmxaRkGLbN54ugeeJ5AfY6OgAzTT71MZ=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "inteligencialtda",
                    "url": "https://www.youtube.com/@inteligencialtda",
                    "avatar": "https://yt3.googleusercontent.com/2GryOij-GwwiaE0MlkB-wZPYRG-wVZNsClgFQIjukKWImTAa1JS-EfJBwqsWbwIyMFJ3lGApxQ=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "ParlapataoQueEs",
                    "url": "https://www.youtube.com/@ParlapataoQueEs",
                    "avatar": "https://yt3.googleusercontent.com/WeACnL5E-8MtZHflyTV33zrjDe8i8pjnhUT0qbcXYllgzFWOFushIJvc8TlOrtru5MhbSFUP=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "revistaISTOE",
                    "url": "https://www.youtube.com/@revistaISTOE",
                    "avatar": "https://yt3.googleusercontent.com/Z89uT6mT2Pi3Tj62ijsj_WOcDJQsOPywjopRsYoCguk0oU-qZhz0-4V-MeMURvszZec59nx_pg=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "Kazam09",
                    "url": "https://www.youtube.com/@Kazam09",
                    "avatar": "https://yt3.googleusercontent.com/ecG6ZLoWmvS1Vx9upXTw9shMTXdOLflVgqyEPQs0c5POJUl86Bnu-JiTpblGOOGdLHKhCDITMSI=s160-c-k-c0x00ffffff-no-rj",
                },
            ],
        },
        {
            "avatar": "https://yt3.googleusercontent.com/ecG6ZLoWmvS1Vx9upXTw9shMTXdOLflVgqyEPQs0c5POJUl86Bnu-JiTpblGOOGdLHKhCDITMSI=s160-c-k-c0x00ffffff-no-rj",
            "name": "Kazam09",
            "url": "https://www.youtube.com/@Kazam09",
            "fonts": [
                {
                    "name": "TodeMOTOPodcast",
                    "url": "https://www.youtube.com/@TodeMOTOPodcast",
                    "avatar": "https://yt3.googleusercontent.com/Y1vwq5ulxeRA5JXThkMwmM8_DwJS6fKZpSUkzX9TsMScr3_YcUcB_9HVppFcN_08ewb-3xmrzw=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "inteligencialtda",
                    "url": "https://www.youtube.com/@inteligencialtda",
                    "avatar": "https://yt3.googleusercontent.com/2GryOij-GwwiaE0MlkB-wZPYRG-wVZNsClgFQIjukKWImTAa1JS-EfJBwqsWbwIyMFJ3lGApxQ=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "ParlapataoQueEs",
                    "url": "https://www.youtube.com/@ParlapataoQueEs",
                    "avatar": "https://yt3.googleusercontent.com/WeACnL5E-8MtZHflyTV33zrjDe8i8pjnhUT0qbcXYllgzFWOFushIJvc8TlOrtru5MhbSFUP=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "revistaISTOE",
                    "url": "https://www.youtube.com/@revistaISTOE",
                    "avatar": "https://yt3.googleusercontent.com/Z89uT6mT2Pi3Tj62ijsj_WOcDJQsOPywjopRsYoCguk0oU-qZhz0-4V-MeMURvszZec59nx_pg=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "Kazam09",
                    "url": "https://www.youtube.com/@Kazam09",
                    "avatar": "https://yt3.googleusercontent.com/ecG6ZLoWmvS1Vx9upXTw9shMTXdOLflVgqyEPQs0c5POJUl86Bnu-JiTpblGOOGdLHKhCDITMSI=s160-c-k-c0x00ffffff-no-rj",
                },
            ],
        },
        {
            "avatar": "https://yt3.googleusercontent.com/ecG6ZLoWmvS1Vx9upXTw9shMTXdOLflVgqyEPQs0c5POJUl86Bnu-JiTpblGOOGdLHKhCDITMSI=s160-c-k-c0x00ffffff-no-rj",
            "name": "Kazam09",
            "url": "https://www.youtube.com/@Kazam09",
            "fonts": [
                {
                    "name": "TodeMOTOPodcast",
                    "url": "https://www.youtube.com/@TodeMOTOPodcast",
                    "avatar": "https://yt3.googleusercontent.com/Y1vwq5ulxeRA5JXThkMwmM8_DwJS6fKZpSUkzX9TsMScr3_YcUcB_9HVppFcN_08ewb-3xmrzw=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "inteligencialtda",
                    "url": "https://www.youtube.com/@inteligencialtda",
                    "avatar": "https://yt3.googleusercontent.com/2GryOij-GwwiaE0MlkB-wZPYRG-wVZNsClgFQIjukKWImTAa1JS-EfJBwqsWbwIyMFJ3lGApxQ=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "ParlapataoQueEs",
                    "url": "https://www.youtube.com/@ParlapataoQueEs",
                    "avatar": "https://yt3.googleusercontent.com/WeACnL5E-8MtZHflyTV33zrjDe8i8pjnhUT0qbcXYllgzFWOFushIJvc8TlOrtru5MhbSFUP=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "revistaISTOE",
                    "url": "https://www.youtube.com/@revistaISTOE",
                    "avatar": "https://yt3.googleusercontent.com/Z89uT6mT2Pi3Tj62ijsj_WOcDJQsOPywjopRsYoCguk0oU-qZhz0-4V-MeMURvszZec59nx_pg=s160-c-k-c0x00ffffff-no-rj",
                },
                {
                    "name": "Kazam09",
                    "url": "https://www.youtube.com/@Kazam09",
                    "avatar": "https://yt3.googleusercontent.com/ecG6ZLoWmvS1Vx9upXTw9shMTXdOLflVgqyEPQs0c5POJUl86Bnu-JiTpblGOOGdLHKhCDITMSI=s160-c-k-c0x00ffffff-no-rj",
                },
            ],
        },
    ]
    return render(request, "sources.html", {"sources": data})


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("", home),
    path("sources", sources),
    path("channels", channels),
]

urlpatterns += [
    path("__reload__/", include("django_browser_reload.urls")),
]


application = get_wsgi_application()

if __name__ == "__main__":
    execute_from_command_line(["manage.py", "runserver"])
