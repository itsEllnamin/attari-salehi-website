from django.contrib import admin
from .models import DiscountCode, DiscountBasket, DiscountBasketDetail


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('discount_code', 'start_datetime', 'end_datetime', 'discount_percent', 'is_active')
    ordering = ('is_active', 'discount_percent')

class DiscountBasketDetailInlineAdmin(admin.TabularInline):
    model = DiscountBasketDetail
    extra = 3

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'end_datetime', 'discount_percent', 'is_active')
    ordering = ('is_active', 'discount_percent')
    inlines = [DiscountBasketDetailInlineAdmin]