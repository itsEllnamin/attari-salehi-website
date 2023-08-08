from django.urls import path
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('remember_password/', RememberPasswordView.as_view(), name='remember_password'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('user_panel/', UserPanelView.as_view(), name='user_panel'),
    path('show_last_orders/', show_last_orders, name='last_orders'),
    path('show_payments/', show_payments, name='show_payments'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    
]
