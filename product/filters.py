from django_filters import rest_framework as filters

from product.models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains') 
    price = filters.NumberFilter()
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    sizes_name = filters.CharFilter(field_name='sizes__name',lookup_expr='iexact')
    colors_name = filters.CharFilter(field_name='colors__name',lookup_expr='iexact')
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    # category__name =

    class Meta:
        model = Product
        fields = ["category","sub_categories",]

    # def rating_method(self, queryset, name, value):
    #     return queryset.filter(rating__gte=value)