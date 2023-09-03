from django.contrib import admin
from django.db.models.aggregates import Count
from admin_decorators import order_field
from .models import (
    ProductCategory,
    ProductFeature,
    ProductImage,
    Product,
    Feature,
    # Brand,
    FeatureDigitalValue
)


# ===================================== ProductCategory ========================================
# ------------------------------ methods ----------------------------------


# ------------------------------ classes ----------------------------------
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "subset_of", "subsets_value", "products_count", "is_active", "update_datetime")
    list_editable = ["is_active"]
    inlines = (ProductGroupInstanceInlineAdmin,)
    
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductCategoryAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(subsets_count=Count('subsets'))
        qs = qs.annotate(products=Count('category_products'))
        return qs

    @order_field ('products')  
    def products_count(self, obj):
        return obj.products

    @order_field('subsets_count')
    def subsets_value(self, obj):
        return ', '.join([subset.title for subset in obj.subsets.filter(is_active=True)])

    subsets_value.short_description = 'زیرمجموعه‌ها'
    products_count.short_description = 'تعداد کالاها'
# ===================================== Product ================================================
# ------------------------------ methods ----------------------------------


# ------------------------------ classes ----------------------------------
class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 5

    class Media:
        js = (
            "vendor/jquery-3.3.1/jquery.min.js",
            "js/admin_script.js",
        )


class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "category",
        # "brand",
        "is_active",
        "update_datetime",
    )
    search_fields = ("name",)
    list_editable = ["is_active"]
    inlines = (ProductFeatureInlineAdmin, ProductGalleryInlineAdmin)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = ProductCategory.objects.filter(subsets=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ===================================== Brand ================================================
# ------------------------------ methods ----------------------------------

# ------------------------------ classes ----------------------------------


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ("title", "logo", "is_active", "update_datetime")
#     list_editable = ["is_active"]


# ===================================== Feature ================================================
# ------------------------------ methods ----------------------------------

# ------------------------------ classes ----------------------------------

class FeatureDigitalValueInlineAdmin(admin.TabularInline):
    model = FeatureDigitalValue
    extra = 3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "display_product_categories", "display_digital_values", "is_active", "update_datetime")
    list_editable = ["is_active"]
    inlines = [FeatureDigitalValueInlineAdmin]


    def get_queryset(self, *args, **kwargs):
        qs = super(FeatureAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(categories_count=Count('categories'))
        qs = qs.annotate(digital_values_count=Count('digital_values'))
        return qs

    @order_field('digital_values_count')   
    def display_digital_values(self, obj):
        return ', '.join([digital_values.value  for digital_values in obj.digital_values.all()])
    
    @order_field('categories_count')
    def display_product_categories(self, obj):
        return ', '.join([category.title for category in obj.categories.filter(is_active=True)])
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'categories':
            kwargs['queryset'] = ProductCategory.objects.filter(subsets=None)
        return super().formfield_for_manytomany(db_field, request, **kwargs)    

    display_product_categories.short_description = 'دسته‌های مرتبط'
    display_digital_values.short_description = 'مقادیر دیجیتال'