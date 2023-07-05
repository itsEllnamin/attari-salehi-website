from django.urls import path
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
]
