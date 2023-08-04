from django.urls import path
from .views import IndexView, slider


app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sliders/', slider, name='sliders'),
]
