from django.urls import path
from coupons.views import ClientCouponListView, CartCouponListView



# router.register(r'articles', ClientArticleModelViewset)


urlpatterns = [
    path("",ClientCouponListView.as_view(), name="all_coupons"),
    path("order/<uid>/",CartCouponListView.as_view(), name="all_coupons_cart"),
]
