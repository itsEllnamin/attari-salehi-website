from django.contrib import admin
from apps.orders.models import PaymentType


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_type')