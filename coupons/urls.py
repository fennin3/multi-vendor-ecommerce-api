from django.urls import path,include
from rest_framework import routers

from coupons.views import CouponAdminModelViewset


router = routers.DefaultRouter(trailing_slash=True)

router.register(r'coupons', CouponAdminModelViewset)

# router.register(r'articles', ClientArticleModelViewset)


urlpatterns = [
    path('', include(router.urls)),
]
