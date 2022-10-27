from django_filters import rest_framework as filters
from order.models import OrderItem

from product.models import Product


class OrderItemFilter(filters.FilterSet):
    ordered = filters.DateFromToRangeFilter(field_name="ordered_date")
    confirmed = filters.DateFromToRangeFilter(field_name="confirmed_date")
    shipped = filters.DateFromToRangeFilter(field_name="shipped_date")
    delivered = filters.DateFromToRangeFilter(field_name="delivered_date")
    cancelled = filters.DateFromToRangeFilter(field_name="cancelled_date")
    refunded = filters.DateFromToRangeFilter(field_name="refunded_date")
    returned = filters.DateFromToRangeFilter(field_name="returned_date")

    class Meta:
        model = OrderItem
        fields = ("status",)
