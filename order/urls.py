from django.urls import path
from .views import AnnualSalesTotal, DailySalesTotal, MonthlySalesTotal, UpdateOrderStatus,\
     VendorAllOrder, VendorArrivedOrder, VendorOrder,\
     add_to_cart

urlpatterns = [
    path("add-to-cart/",add_to_cart, name="add_to_cart"),
    path('<status>/', VendorOrder.as_view(),name="vendor_orders"),
    # path('shipped-orders/', VendorShippedOrder.as_view(),name="vendor_orders"),
    path('all-orders/', VendorAllOrder.as_view(),name="vendor_orders"),
    path('arrived-orders/', VendorArrivedOrder.as_view(),name="vendor_orders"),
    path('daily-total/', DailySalesTotal.as_view(),name="daily_total"),
    path('monthly-total/', MonthlySalesTotal.as_view(),name="month_total"),
    path('annual-total/', AnnualSalesTotal.as_view(),name="annual_total"),
    path('order-shipped/', UpdateOrderStatus.as_view(),name="vendor_orders"),
]