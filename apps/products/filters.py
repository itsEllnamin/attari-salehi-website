import django_filters
from .models import Product, FeatureDigitalValue



class ProductFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request', None)
        request.session['feature_value_list'] = request.GET.getlist('feature_value')
        request.session['price_min'] = request.GET.get('price_min')
        request.session['price_max'] = request.GET.get('price_max')
        queryset = kwargs.get('queryset', None)
        self.declared_filters['feature_value'].queryset = FeatureDigitalValue.objects.filter(feature__categories__id__icontains=queryset[0].category.id)
        super().__init__(*args, **kwargs)
        
        
    price = django_filters.RangeFilter(
        "price",
    )
    feature_value = django_filters.ModelMultipleChoiceFilter(
        field_name="product_features__digital_value",
        # distinct = True
    )

    class Meta:
        model = Product
        fields = ["price", "feature_value"]
