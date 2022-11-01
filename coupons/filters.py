from django_filters import rest_framework as filters
from coupons.models import Coupon, UsedCoupon



class CouponFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title",lookup_expr='icontains') 
    code = filters.CharFilter(field_name="code", lookup_expr='icontains')
    is_active = filters.BooleanFilter() 
    min_available = filters.NumberFilter(field_name="available_coupons", lookup_expr="gte")
    max_available = filters.NumberFilter(field_name="available_coupons", lookup_expr="lte")

    sort_by = filters.OrderingFilter(fields=(
            ('title', 'title'),
            ('created_at', 'created_at'),
        ))

    class Meta:
        model = Coupon
        fields = ("product","is_active", "condition", "discount_type", "available_coupons")