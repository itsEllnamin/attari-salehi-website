from django.urls import path
from . import views


app_name = 'discounts'

urlpatterns = [
    path('apply_discount_code/<int:order_id>/', views.ApplyDiscountCode.as_view(), name='apply_discount_code'),
]
