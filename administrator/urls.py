from django.urls import path, include
from rest_framework import routers

from .views import (ActiveCustomer, ActiveInactiveBankDetail, AddSiteAddress, AdminProfile, AllOrders, AllSubscribers, AnnualOrdersSummary, ApproveDOTD, ApproveFlashSaleRequest,
 ApproveProduct,  BankDetailsView, BannerStatus, BannerViewSets, CategoryViewSet, ColorModelViewset, ConfirmAccount, CountryView, CountsAnalytics, 
 CreateListShippingZonesView, CustomerViewSet, DailyOrdersSummary, 
 DisapproveProduct, ListContactMessages, ListandCreateAdmin, AdminLogin, MonthlyOrdersSummary, ProductViewSet, \
 RetrieveCustomerOrder, RetrieveFlashSaleRequest, RetrieveRemoveUpdateDOTD, RetrieveUpdateDestroyAdminView, SizeModelViewset, SocialMediaStatus, SocialMediaViewSet, SubCategoryViewSet, SuspendUnsuspendCustomer,\
     SuspendVendor, TestimonialViewSet, UpdateAddress, UpdateDeleteRetrieveFlashSaleRequest, UpdateFeatured, UpdateOrderStatus, VendorViewSet, VerifyUnverifyBankDetail)

from blog.views import ArticleCategoryModelViewset, ArticleModelViewset, CommentModelViewset, CommentReplyModelViewset


router = routers.DefaultRouter(trailing_slash=True)
router.register(r'vendors', VendorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'zones', CreateListShippingZonesView)
router.register(r'countries', CountryView)
router.register(r'customers', CustomerViewSet)
router.register(r'banners', BannerViewSets)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'social-media', SocialMediaViewSet)
router.register(r'sizes', SizeModelViewset)
router.register(r'colors', ColorModelViewset)

router.register(r'blog/articles', ArticleModelViewset)

router.register(r'blog/categories', ArticleCategoryModelViewset)
router.register(r'blog/comments', CommentModelViewset)
router.register(r'blog/replies', CommentReplyModelViewset)



urlpatterns = [
    path('', ListandCreateAdmin.as_view(), name='list_and_create_admin'),
    path('signin/', AdminLogin.as_view(), name='admin_login'),

    path('profile/', AdminProfile.as_view(), name='admin_profile'),

    path('orders/', AllOrders.as_view(), name='orders'),

    path('social-media/<uid>/status/', SocialMediaStatus.as_view(), name='social_media_status'),

    path('subscribers/', AllSubscribers.as_view(), name='subs'),

    path('contact-messages/', ListContactMessages.as_view(), name='contact_messages'),


    path('banners/<uid>/status/', BannerStatus.as_view(), name='banner_status'),


    path('products/<uid>/featured/', UpdateFeatured.as_view(), name='orders'),

    path('flash-requests/', RetrieveFlashSaleRequest.as_view(), name='list_flash_requests'),
    path('flash-requests/<uid>/status/', ApproveFlashSaleRequest.as_view(), name='status_flash_requests'),

    path('flash-requests/<uid>/', UpdateDeleteRetrieveFlashSaleRequest.as_view(), name='update_flash_requests'),

    # path('orders/placed_orders/', OrderedOrders.as_view(), name='new_orders'),
    # path('orders/processed_orders/', ProcessedOrders.as_view(), name='processed_orders'),
    # path('orders/shipped_orders/', ShippedOrders.as_view(), name='shipped_orders'),
    # path('orders/delivered_orders/', DeliveredOrders.as_view(), name='delivered_orders'),
    # path('orders/cancelled_orders/', CancelledOrders.as_view(), name='delivered_orders'),
    # path('orders/confirmed_orders/', ConfirmedOrders.as_view(), name='confirmed_orders'),
    # path('orders/returned_orders/', ReturnedOrders.as_view(), name='returned_orders'),
    # path('orders/refunded_orders/', RefundededOrders.as_view(), name='refunded_orders'),


    path('accounts/', ListandCreateAdmin.as_view(), name='list_create_admin'),
    path('accounts/confirm/', ConfirmAccount.as_view(), name='confirm_account'),
    path('accounts/<user__uid>/', RetrieveUpdateDestroyAdminView.as_view(), name='update_admin'),


    path('customers/<uid>/suspend/', SuspendUnsuspendCustomer.as_view(), name='customer_suspend'),
    path('customers/<uid>/status/', ActiveCustomer.as_view(), name='customer_status'),
    path('customers/<uid>/orders/', RetrieveCustomerOrder.as_view(), name='customer_orders'),

    path('orders/analytics/daily/', DailyOrdersSummary.as_view(), name="daily_summary"),
    path('orders/analytics/monthly/', MonthlyOrdersSummary.as_view(), name="monthly_summary"),
    path('orders/analytics/yearly/', AnnualOrdersSummary.as_view(), name="year_summary"),

    path('orders/analytics/counts/', CountsAnalytics.as_view(), name="summary_counts"),

    
    
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