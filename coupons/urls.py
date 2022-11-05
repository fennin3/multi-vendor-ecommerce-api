from django.urls import path
from coupons.views import ApplyCoupon, ClientCouponListView, CartCouponListView



# router.register(r'articles', ClientArticleModelViewset)


urlpatterns = [
    path("",ClientCouponListView.as_view(), name="all_coupons"),
    path("apply/",ApplyCoupon.as_view(), name="apply_coupons"),
    path("order/<uid>/",CartCouponListView.as_view(), name="all_coupons_cart"),
]
