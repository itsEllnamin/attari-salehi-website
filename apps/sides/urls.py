from django.urls import path
from . import views


app_name = 'sides'

urlpatterns = [
   path('add_score/', views.add_score, name='add_score'),
   path('create_comment/<slug:slug>/', views.CreateCommentView.as_view(), name='create_comment'),
   path('favorites/', views.FavoriteView.as_view(), name='favorites'),
   path('favorites_detail/', views.favorites_detail, name='favorites_detail'),
   path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
   path('delete_from_favorites/', views.delete_from_favorites, name='delete_from_favorites'),
   path('favorites_status/', views.favorites_status, name='favorites_status'),
   path('search', views.SearchView.as_view(), name='search'),
]
