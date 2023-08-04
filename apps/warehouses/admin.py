from django.contrib import admin
from .models import Transaction, TransactionType


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'type', 'price', 'qty']
