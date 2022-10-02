from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from administrator.views import ListCountries

urlpatterns = [
    path('admin-dashboard/', admin.site.urls),
    path('vendors/', include('vendor.urls')),
    path('customers/', include('customer.urls')),
    path('administrators/', include('administrator.urls')),
    path('products/', include('product.urls')),
    path('transactions/',include('transactions.urls')),
    path('orders/',include('order.urls')),
    path('countries/', ListCountries.as_view(), name="countries"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
'''
    path('products/', include('product.urls')),
    path('orders/', include('order.urls')),
    path('wallet/', include('wallet.urls'))
    '''