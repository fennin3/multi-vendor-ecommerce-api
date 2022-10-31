from django_filters import rest_framework as filters
from order.models import Order

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
    is_active = filters.BooleanFilter()
    is_approved = filters.BooleanFilter()
    sub_categories = filters.UUIDFilter(field_name="sub_categories")
    date = filters.DateTimeFromToRangeFilter(field_name='created_at')
    sort_by = filters.OrderingFilter(fields=(
            ('name', 'name'),
            ('price', 'price'),
        ))

    class Meta:
        model = Product
        fields = ["category","sub_categories", 'is_active', 'is_approved', 'created_at']


class OrderFilter(filters.FilterSet):
    ordered = filters.DateFromToRangeFilter(field_name="ordered_date")
    confirmed = filters.DateFromToRangeFilter(field_name="confirmed_date")
    shipped = filters.DateFromToRangeFilter(field_name="shipped_date")
    delivered = filters.DateFromToRangeFilter(field_name="delivered_date")
    cancelled = filters.DateFromToRangeFilter(field_name="cancelled_date")
    refunded = filters.DateFromToRangeFilter(field_name="refunded_date")
    returned = filters.DateFromToRangeFilter(field_name="returned_date")


    class Meta:
        model = Order
        fields = ("status",)