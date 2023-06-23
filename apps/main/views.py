from django.conf import settings
from django.shortcuts import render


def media_admin(request):
    return {'media_url': settings.MEDIA_URL,}

def index(request):
    return render(request, 'main/index.html')