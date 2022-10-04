from django.urls import path

from .views import (CreateDealOfTheRequestView, DeleteUpdateRetrieveDealOfTheRequestView, VendorCloseOrOpen, VendorList, VendorDetail, ConfirmAccount, VendorLogin, VendorProfile, VendorUpdate)


urlpatterns = [
    path('', VendorList.as_view(), name='all_vendors'),
    path('signin/', VendorLogin.as_view(), name='sign_in'), 
    path('confirm-account/', ConfirmAccount.as_view(), name='confirm_account'),
    path('close-open/', VendorCloseOrOpen.as_view(), name='close_open'),
    path('deals/requests/', CreateDealOfTheRequestView.as_view(), name='deal_of_the_day'),
    path('deals/requests/<uid>/', DeleteUpdateRetrieveDealOfTheRequestView.as_view(), name='deal_of_the_day'),
    path('<user__uid>/', VendorDetail.as_view(), name='vendor_detail'),
    path('<user__uid>/update/', VendorUpdate.as_view(), name='vendor_update'),
    path('dashboard/', VendorProfile.as_view(), name='vendor_dashboard')
]