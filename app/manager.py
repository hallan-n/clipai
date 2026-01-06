import os
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

# ======================
# CONFIGURAÇÕES
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY="dev-secret-key",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        "django.middleware.common.CommonMiddleware",
    ],
)

# ======================
# VIEW
# ======================
def home(request):
    return HttpResponse("<h1>Olá, Django em um arquivo ssdsdó!</h1>")

# ======================
# URLS
# ======================
urlpatterns = [
    path("", home),
]

# ======================
# START
# ======================
application = get_wsgi_application()

if __name__ == "__main__":
    execute_from_command_line(["manage.py", "runserver"])
