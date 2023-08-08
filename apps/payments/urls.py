from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('zarinpal_payment/<int:order_id>', views.ZarinpalPaymentView.as_view(), name='zarinpal_payment'),
    path('verify_zarinpal_payment/', views.ZarinpalPaymentVerifyView.as_view(), name='verify_zarinpal_payment'),
    path('show_verification_message/<str:message>/', views.show_verification_message, name='show_verification_message'),
]
