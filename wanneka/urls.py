from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from administrator.views import ListCountries, GetSiteInfo,UpdateSiteInfo
from vendor.views import CustomUserDetail

urlpatterns = [
    path('admin-dashboard/', admin.site.urls),
    path('vendors/', include('vendor.urls')),
    path('customers/', include('customer.urls')),
    path('administrators/', include('administrator.urls')),
    path('products/', include('product.urls')),
    path('transactions/',include('transactions.urls')),
    path('orders/',include('order.urls')),

    # General Info
    path('countries/', ListCountries.as_view(), name="countries"),


    path('users/update/<uid>/', CustomUserDetail.as_view(), name="update_user"),

    # Site Info
    path("config/", GetSiteInfo.as_view(), name="get_site_info"),
    path("config/update/", UpdateSiteInfo.as_view(), name="update_site_info"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
'''
    path('products/', include('product.urls')),
    path('orders/', include('order.urls')),
    path('wallet/', include('wallet.urls'))
    '''