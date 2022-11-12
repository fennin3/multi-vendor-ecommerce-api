from django.urls import path
from .views import AddAddressToCart, AnnualSalesTotal, ClientRetriveOrder, DailySalesTotal, MonthlySalesTotal, RemoveAddressToCart, UpdateOrderStatus,\
    VendorArrivedOrder, VendorOrder, RevenueBasedonArea,\
     add_to_cart, remove_from_cart,set_item_quantity, substract_item_quantity, add_item_quantity

urlpatterns = [
    path('', VendorOrder.as_view(),name="vendor_orders"),
    path("add-to-cart/",add_to_cart, name="add_to_cart"),
    path("add-quantity/",add_item_quantity, name="add_quantity"),
    path("remove-item/",remove_from_cart, name="remove_item"),
    path("set-quantity/",set_item_quantity, name="set_item"),
    path("subtract-quantity/",substract_item_quantity, name="sub_item"),
    path("cart/", ClientRetriveOrder.as_view(), name="client_user"),

    # To Be Documented
    path("add-address/", AddAddressToCart.as_view(), name="add_address"),
    path("remove-address/", RemoveAddressToCart.as_view(), name="remove_address"),

    
    path('arrived-orders/', VendorArrivedOrder.as_view(),name="vendor_orders"),
    path('daily-total/', DailySalesTotal.as_view(),name="daily_total"),
    path('monthly-total/', MonthlySalesTotal.as_view(),name="month_total"),
    path('annual-total/', AnnualSalesTotal.as_view(),name="annual_total"),
    path('area-revenue/', RevenueBasedonArea.as_view(),name="annual_total"),
    path('order-shipped/', UpdateOrderStatus.as_view(),name="vendor_orders"),
]