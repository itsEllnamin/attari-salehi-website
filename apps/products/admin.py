from django.contrib import admin
from . import models



@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'subset_of', 'is_active', 'update_datetime')
    list_editable = ['is_active']
    
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'brand', 'is_active', 'update_datetime')
    list_editable = ['is_active']
    
    
@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'logo', 'is_active', 'update_datetime')
    list_editable = ['is_active']
    
    
@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'update_datetime')
    list_editable = ['is_active']

