from django.conf import settings
from django.views.generic import TemplateView
from utils import page_path
from apps.products.models import ProductCategory



appname = 'main'

def media_admin(request):
    return {'media_url': settings.MEDIA_URL,}

def navbar_categories(request):
    return{'root_categories': ProductCategory.get_root_categories()}

class IndexView(TemplateView):
    template_name = page_path(appname, 'index')