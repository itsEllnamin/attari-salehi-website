from django.contrib import admin
from .models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('image_slide', 'title1', 'link', 'is_active', 'register_datetime')
    list_filter = ('register_datetime',)
    search_fields = ('title1',)
    ordering = ('-register_datetime',)
    readonly_fields = ('image_slide',)