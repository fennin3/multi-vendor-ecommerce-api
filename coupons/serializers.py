from rest_framework.serializers import ModelSerializer

from coupons.models import Coupon, UsedCoupon


class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields="__all__"


        extra_kwargs = {
            "is_active":{"default":True}
        }

class CouponUsedSerializer(ModelSerializer):
    class Meta:
        model = UsedCoupon
        fields="__all__"