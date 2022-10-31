from django_filters import rest_framework as filters

from product.models import Category, Product, SubCategory


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains') 
    price = filters.NumberFilter()
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    sizes_name = filters.CharFilter(field_name='sizes__name',lookup_expr='iexact')
    colors_name = filters.CharFilter(field_name='colors__name',lookup_expr='iexact')
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    sub_categories = filters.UUIDFilter(field_name="sub_categories")
    sort_by = filters.OrderingFilter(fields=(
            ('name', 'name'),
            ('price', 'price'),
        ))

    class Meta:
        model = Product
        fields = ("category",)

class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains') 

    class Meta:
        model = Category
        fields = ()

class SubCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains') 

    class Meta:
        model = SubCategory
        fields = ("category",)

