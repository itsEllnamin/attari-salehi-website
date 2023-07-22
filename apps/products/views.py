from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, JsonResponse
from .models import Product, ProductCategory, FeatureDigitalValue
from .filters import ProductFilter
from django.db.models import Count, Q, Max, Min
from django.views import View
from utils import partial_path, page_path
from django_filters.views import FilterView


appname = "products"

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


# برگرداندن یک محصول
def get_product(slug):
    return get_object_or_404(Product, is_active=True, slug=slug)


# برگرداندن یک دسته محصول
def get_product_category(slug):
    return get_object_or_404(ProductCategory, is_active=True, slug=slug)


# برگرداندن دسته‌های دارای محصول جهت نمایش
def get_categories_contain_products():
    return ProductCategory.objects.filter(is_active=True, subsets=None)


# برگرداندن محصولات یک دسته
def get_category_products(slug):
    category = get_product_category(slug)
    queryset = Product.objects.filter(is_active=True, category=category)
    return queryset


# =============================== Partials ==================================


# # ارزان‌ترین محصولات
class CheapestProductsView(TemplateView):
    template_name = partial_path(appname, "show_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by("price")
        context["categories"] = get_categories_contain_products()
        context["group_name"] = "ارزان‌ترین محصولات"
        context["ad"] = True
        context["type"] = "row"
        return context


# # جدیدترین محصولات
class NewestProductsView(TemplateView):
    template_name = partial_path(appname, "show_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-publish_datetime"
        )[:5]
        context["group_name"] = "جدیدترین محصولات"
        context["ad"] = True
        context["type"] = "column"
        return context


# # محصولات مرتبط
class RelatedProductsView(TemplateView):
    template_name = partial_path(appname, "show_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_product(kwargs["slug"])
        context["products"] = Product.objects.filter(
            ~Q(id=product.id), is_active=True, category=product.category
        )
        context["group_name"] = "محصولات مرتبط"
        context["ad"] = True
        context["type"] = "row"
        return context


# # نمایش محصولات یک دسته‌بندی
# class CategoryProductsView(FilterView):
#     model = Product
#     filterset_class = ProductFilter
#     paginate_by = 9
#     template_name = partial_path(appname, "show_products")

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         slug = self.kwargs.get('slug')
#         if slug:
#             queryset = get_category_products(slug)

#         return queryset


# # نمایش دسته‌های کالا
class CategoriesView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            get_categories_contain_products()
            .annotate(products_count=Count("category_products"))
            .order_by("-products_count")
        )
        return context

    template_name = partial_path(appname, "categories")


# =============================== Pages ==================================


class ProductView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = get_product(kwargs["slug"])
        return context

    template_name = page_path(appname, "product")


class ProductCategoryView(FilterView):
    model = Product
    template_name = page_path(appname, "category")
    filterset_class = ProductFilter
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feature_value_list = self.request.session.get('feature_value_list')
        price_max = self.request.session.get('price_max')
        price_min = self.request.session.get('price_min')
        slug = self.kwargs.get("slug")
        context['feature_value_list'] = [int(item) for item in feature_value_list]
        context['price_max'] = price_max
        context['price_min'] = price_min
        context["current_category"] = get_product_category(slug)
        context["categories"] = (
            get_categories_contain_products()
            .annotate(
                count=Count("category_products"),
                min_p=Min("category_products__price"),
                max_p=Max("category_products__price"),
                mid_p=(Min("category_products__price")+(Max("category_products__price")))/2
            )
            .order_by("-count")
        )
        return context

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = get_category_products(slug)

        return queryset


# ================================ Ajax ==================================


# برگرداندن مقادیر دیجیتال یک ویژگی (ajax)
def get_feature_digital_values(request):
    if request.method == "GET":
        feature_id = request.GET.get("feature_id")
        feature_values = FeatureDigitalValue.objects.filter(feature_id=feature_id)
        res = {fv.value: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)
