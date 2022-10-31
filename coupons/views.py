from rest_framework.viewsets import ModelViewSet
from coupons.filters import CouponFilter

from coupons.models import Coupon, UsedCoupon
from coupons.serializers import CouponSerializer
from administrator.permissions import IsSuperuser
from vendor.paginations import AdminVendorPagination

from django_filters import rest_framework as filters

class CouponAdminModelViewset(ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permission_classes = (IsSuperuser,)
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CouponFilter
