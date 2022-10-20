from django.urls import path
from django.urls import path, include
from rest_framework import routers

from .views import (ActiveCustomer, ActiveInactiveBankDetail, AddProductToFlashSales, AddSiteAddress, AllOrders, AnnualOrdersSummary, ApproveDOTD,
 ApproveProduct,  BankDetailsView, CancelledOrders, CategoryViewSet, ConfirmAccount, ConfirmedOrders, CountryView, 
 CreateListShippingZonesView, CustomerViewSet, DailyOrdersSummary, DeclineDOTDRequest, DeliveredOrders, 
 DisapproveProduct, ListandCreateAdmin, AdminLogin, MonthlyOrdersSummary, OrderedOrders, ProductViewSet, RefundededOrders,
  RetrieveApprovedDealOfTheDayRequests, RetrieveCustomerOrder, RetrievePendingDealOfTheDayRequests, ProcessedOrders, RetrieveRemoveUpdateDOTD, RetrieveUpdateDestroyAdminView, 
  ReturnedOrders, ShippedOrders, SubCategoryViewSet, SuspendUnsuspendCustomer, SuspendVendor, UpdateAddress, UpdateFeatured, UpdateOrderStatus, VendorViewSet, VerifyUnverifyBankDetail)


router = routers.DefaultRouter(trailing_slash=True)
router.register(r'vendors', VendorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'zones', CreateListShippingZonesView)
router.register(r'countries', CountryView)
router.register(r'customers', CustomerViewSet)



urlpatterns = [
    path('', ListandCreateAdmin.as_view(), name='list_and_create_admin'),
    path('signin/', AdminLogin.as_view(), name='admin_login'),
    path('orders/', AllOrders.as_view(), name='orders'),


    path('products/<uid>/featured/', UpdateFeatured.as_view(), name='orders'),

    path('add-flashsale/', AddProductToFlashSales.as_view(), name='add_flash_sale'),

    path('orders/placed_orders/', OrderedOrders.as_view(), name='new_orders'),
    path('orders/processed_orders/', ProcessedOrders.as_view(), name='processed_orders'),
    path('orders/shipped_orders/', ShippedOrders.as_view(), name='shipped_orders'),
    path('orders/delivered_orders/', DeliveredOrders.as_view(), name='delivered_orders'),
    path('orders/cancelled_orders/', CancelledOrders.as_view(), name='delivered_orders'),
    path('orders/confirmed_orders/', ConfirmedOrders.as_view(), name='confirmed_orders'),
    path('orders/returned_orders/', ReturnedOrders.as_view(), name='returned_orders'),
    path('orders/refunded_orders/', RefundededOrders.as_view(), name='refunded_orders'),


    path('accounts/', ListandCreateAdmin.as_view(), name='list_create_admin'),
    path('accounts/confirm/', ConfirmAccount.as_view(), name='confirm_account'),
    path('accounts/<user__uid>/', RetrieveUpdateDestroyAdminView.as_view(), name='update_admin'),


    path('customers/<uid>/suspend/', SuspendUnsuspendCustomer.as_view(), name='customer_suspend'),
    path('customers/<uid>/status/', ActiveCustomer.as_view(), name='customer_status'),
    path('customers/<uid>/orders/', RetrieveCustomerOrder.as_view(), name='customer_orders'),

    path('orders/analytics/daily/', DailyOrdersSummary.as_view(), name="daily_summary"),
    path('orders/analytics/monthly/', MonthlyOrdersSummary.as_view(), name="monthly_summary"),
    path('orders/analytics/yearly/', AnnualOrdersSummary.as_view(), name="year_summary"),

    
    
    path('orders/status/', UpdateOrderStatus.as_view(), name='order_status'),
    # path('deals/pending/', RetrievePendingDealOfTheDayRequests.as_view(), name='unapproved_deals'),
    # path('deals/approved/', RetrieveApprovedDealOfTheDayRequests.as_view(), name='approved_deals'),
    path('deals/', ApproveDOTD.as_view(), name='approve_deals'),
    path('deals/<uid>/', RetrieveRemoveUpdateDOTD.as_view(), name='update_retrieve'),
    # path('deals/decline/', DeclineDOTDRequest.as_view(), name='decline_deals'),
    path('add-address/', AddSiteAddress.as_view(), name='add_address'),
    path('add-address/<pk>/', UpdateAddress.as_view(), name='add_address'),
    path('update-address/', UpdateAddress.as_view(), name='update_address'),
    path('banks/verify/', VerifyUnverifyBankDetail.as_view(), name='bank_verify'),
    path('banks/status/', ActiveInactiveBankDetail.as_view(), name='bank_status'),
    path('vendors/suspend/', SuspendVendor.as_view(), name='suspend_vendor'),
    path('vendors/<uid>/bank-detail/', BankDetailsView.as_view(), name='vendor_bank'),
    path('products/<uid>/approve/', ApproveProduct.as_view(), name='approve_prod'),
    path('products/<uid>/inactive/', DisapproveProduct.as_view(), name='disapprove_prod'),
    path('', include(router.urls)),
]