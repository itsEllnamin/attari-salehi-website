from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'approving_user', 'is_active']
    list_editable = ['is_active', 'approving_user']