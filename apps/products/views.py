from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, JsonResponse
from .models import Product, ProductCategory, FeatureDigitalValue
from .filters import ProductFilter
from django.db.models import Count, Q, Max, Min
from django.views import View
from utils import partial_path, page_path
from django_filters.views import FilterView
from django.db.models import QuerySet


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


# برگرداندن یک دسته‌بندی محصول
def get_product_category(slug):
    return get_object_or_404(ProductCategory, is_active=True, slug=slug)


# برگرداندن دسته‌بندی‌های دارای محصول جهت نمایش
def get_categories_contain_products():
    return ProductCategory.objects.filter(subsets=None)


# برگرداندن محصولات یک دسته‌بندی
def get_category_products(slug):
    category = get_product_category(slug)
    queryset = Product.objects.filter(category=category)
    return queryset


# فیلتر کردن محصولات
def filter_products(*args, **filters):
    return Product.objects.filter(*args, **filters)


# =============================== Classes ==================================
## کلاس‌های زیر بصورت پیشفرض نمونه‌های فعال را در کوئری‌ست
## ذخیره می‌کنند تا در فرزندان آن‌ها از تکرار جلوگیری شود


class ActiveListView(ListView):
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(is_active=True)
        elif self.model is not None:
            queryset = self.model._default_manager.filter(is_active=True)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset
    
    
class ActiveFilterView(FilterView):
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(is_active=True)
        elif self.model is not None:
            queryset = self.model._default_manager.filter(is_active=True)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset
    

class ActiveDetailView(DetailView):
    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.

        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.filter(is_active=True)
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
                )
        return self.queryset.filter(is_active=True)
    
    
# =============================== Partials ==================================


# کلاس بیس محصولات جهت استفاده بعنوان والد در پارشیال‌ها
class BaseProductsView(ActiveListView):
    model = Product
    context_object_name = "products"
    init_context = {"ad": True}
    template_name = partial_path(appname, "show_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.init_context)
        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs[:5]   


# # ارزان‌ترین محصولات
class CheapestProductsView(BaseProductsView):
    ordering = ("price",)
    extra_context = {
        "categories": get_categories_contain_products(),
        "group_name": "ارزان‌ترین محصولات",
         "type": "row"
    }


# # جدیدترین محصولات
class NewestProductsView(BaseProductsView):
    ordering = ("-publish_datetime",)
    extra_context = {"group_name": "جدیدترین محصولات", "type": "column"}


# # محصولات مرتبط
class RelatedProductsView(BaseProductsView):
    extra_context = {"group_name": "محصولات مرتبط",  "type": "row"}

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug", None)
        if slug:
            product = get_product(slug)
            self.queryset = Product.objects.filter(
                ~Q(id=product.id), category=product.category
            )
        queryset = super().get_queryset(**kwargs)
        return queryset


# # نمایش دسته‌بندی‌های محصولات
class CategoriesView(ActiveListView):
    queryset = get_categories_contain_products().annotate(
        products_count=Count("category_products")
    )
    ordering = ('-products_count', )
    context_object_name = 'categories'
    template_name = partial_path(appname, "categories")


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


# =============================== Pages ==================================


class ProductView(ActiveDetailView):
    model = Product
    context_object_name = "product"
    template_name = page_path(appname, "product")

class ProductCategoryView(ActiveFilterView):
    categories = (
        get_categories_contain_products()
        .annotate(
            count=Count("category_products"),
            min_p=Min("category_products__price"),
            max_p=Max("category_products__price"),
            mid_p=(Min("category_products__price") + (Max("category_products__price")))
            / 2,
        )
        .order_by("-count")
    )

    extra_context = {"categories": categories}
    filterset_class = ProductFilter
    paginate_by = 9
    template_name = page_path(appname, "category")
    paginate_orphans = 3

    def get_context_data(self, **kwargs):
        feature_value_list = self.request.session.get("feature_value_list")
        price_max = self.request.session.get("price_max")
        price_min = self.request.session.get("price_min")
        slug = self.kwargs.get("slug")
        context = super().get_context_data(**kwargs)
        context["feature_value_list"] = [int(item) for item in feature_value_list]
        context["price_max"] = price_max
        context["price_min"] = price_min
        context["current_category"] = get_product_category(slug)
        context['sort_type'] = self.sort_type
        return context

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug")
        queryset = get_category_products(slug)
        
        sort_type = self.request.GET.get('sort_type')
        match sort_type:
            case None:
                sort_type = '0'
            case '1':
                self.ordering = ('price',)
            case '2':
                self.ordering = ('-price',)

        self.sort_type = sort_type
        self.queryset = queryset
        return super().get_queryset(**kwargs)


# ================================ Ajax ==================================


# برگرداندن مقادیر دیجیتال یک ویژگی (ajax)
def get_feature_digital_values(request):
    if request.method == "GET":
        feature_id = request.GET.get("feature_id")
        feature_values = FeatureDigitalValue.objects.filter(feature_id=feature_id)
        res = {fv.value: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)
