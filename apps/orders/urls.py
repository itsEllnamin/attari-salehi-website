from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('shop_cart/', views.ShopCartView.as_view(), name='shop_cart'),
    path('shop_cart_status/', views.shop_cart_status, name='shop_cart_status'),
    path('add_to_shop_cart/', views.add_to_shop_cart, name='add_to_shop_cart'),
    path('delete_from_shop_cart/', views.delete_from_shop_cart, name='delete_from_shop_cart'),
    path('update_shop_cart/', views.update_shop_cart, name='update_shop_cart'),
    path('shop_cart_detail/', views.ShopCartDetail.as_view(), name='shop_cart_detail'),
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path('checkout/<int:order_id>/', views.CheckoutOrderView.as_view(), name='checkout'),
]
