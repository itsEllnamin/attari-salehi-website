from django.contrib import admin
from .models import Order, OrderDetail, OrderStatus, PaymentType


class OrderDetailInlineAdmin(admin.TabularInline):
    model = OrderDetail
    extra = 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_status', 'payment_type', 'discount_percent', 'is_finally']
    list_editable = ['order_status']
    inlines = [OrderDetailInlineAdmin]

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
