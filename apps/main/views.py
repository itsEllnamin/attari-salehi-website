from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from utils import page_path, partial_path
from apps.products.models import ProductCategory
from .models import Slider


appname = 'main'

def media_admin(request):
    return {'media_url': settings.MEDIA_URL,}

def request(request):
    return {'request': request}

def navbar_categories(request):
    return{'root_categories': ProductCategory.get_root_categories()}

class IndexView(TemplateView):
    template_name = page_path(appname, 'index')

def slider(request):
    sliders = Slider.objects.filter(is_active=True)
    return render(request, partial_path(appname, 'slider'), {'sliders': sliders})


def handler404(request, exception=None):
    return render(request, 'main/404.html')