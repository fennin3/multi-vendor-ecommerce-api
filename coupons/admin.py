from django.contrib import admin
from coupons.models import Coupon, UsedCoupon


admin.site.register(Coupon)
admin.site.register(UsedCoupon)