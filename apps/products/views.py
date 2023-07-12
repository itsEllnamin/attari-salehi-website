from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import Product, ProductCategory, FeatureDigitalValue
from django.db.models import Count, Q
from django.views import View



# # دسته‌بندی محصولات
# class BaseProductsView(TemplateView):
#     def get_context_data(self, order_by, index, category_name, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.filter(is_active=True).order_by(order_by)[:index]
#         context['product_groups'] = ProductGroup.objects.filter(is_active=True, parent_group=None)
#         context['category_name'] = category_name
#         return context
#     template_name = 'products/partials/show_products.html'

#     class Meta:
#         abstract = True

# =============================== Functions ==================================


def page_path(filename):
    return f"products/{filename}.html"


def partial_path(filename):
    return f"products/partials/{filename}.html"

# برگرداندن یک محصول
def get_product(slug): 
    return get_object_or_404(Product, is_active=True, slug=slug) 

# برگرداندن یک دسته محصول
def get_product_category(slug): 
    return get_object_or_404(ProductCategory, is_active=True, slug=slug) 


# =============================== Partials ==================================
# # ارزان‌ترین محصولات
class CheapestProductsView(TemplateView):
    template_name = partial_path('show_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by("price")
        context["categories"] = ProductCategory.objects.filter(
            is_active=True, subsets=None
        )
        context["group_name"] = "ارزان‌ترین محصولات"
        context["ad"] = True
        context["type"] = "row"
        return context

# # محصولات مرتبط
class RelatedProductsView(TemplateView):
    template_name = partial_path('show_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_product(kwargs['slug'])
        context["products"] = Product.objects.filter(~Q(id=product.id), is_active=True, category=product.category)
        context["group_name"] = "محصولات مرتبط"
        context["ad"] = True
        context["type"] = "row"
        return context

# # محصولات یک دسته‌بندی
class CategoryProductsView(TemplateView):
    template_name = partial_path('show_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_product_category(kwargs['slug'])
        context["products"] = Product.objects.filter(is_active=True, category=category)
        return context


# # # دسته‌بندی جدیدترین محصولات
# class NewestProductsView(BaseProductsView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data('-publish_datetime', 5, 'جدیدترین محصولات')
#         return context


# # # دسته‌بندی گروه‌های محصولات بر اساس تعداد کالا
# class MostMemberedGroupsView(TemplateView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product_groups'] = ProductGroup.objects.filter(is_active=True).annotate(products_count=Count('group_products')).order_by('-products_count')[:6]
#         return context
#     template_name = 'products/partials/categorized_product_groups.html'


# # نمایش دسته‌های کالا
class CategoriesView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            ProductCategory.objects.filter(is_active=True, subsets=None)
            .annotate(products_count=Count("category_products"))
            .order_by("-products_count")
        )
        return context

    template_name = partial_path('categories')


# =============================== Pages ==================================

class ProductView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = get_product(kwargs['slug'])
        return context

    template_name = page_path('product')


class ProductCategoryView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_product_category(kwargs['slug'])
        return context

    template_name = page_path('category')
    

# ================================ Ajax ==================================

# برگرداندن مقادیر دیجیتال یک ویژگی (ajax)
def get_feature_digital_values(request):
    if request.method == "GET":
        feature_id = request.GET.get("feature_id")
        feature_values = FeatureDigitalValue.objects.filter(feature_id=feature_id)
        res = {fv.value: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)
