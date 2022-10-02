from django.urls import path

from .views import (VendorList, VendorDetail, ConfirmAccount, VendorLogin, VendorProfile, VendorUpdate)


urlpatterns = [
    path('', VendorList.as_view(), name='all_vendors'),
    path('signin/', VendorLogin.as_view(), name='sign_in'), 
    path('confirm-account/', ConfirmAccount.as_view(), name='confirm_account'),
    path('<user__uid>/', VendorDetail.as_view(), name='vendor_detail'),
    path('<user__uid>/update/', VendorUpdate.as_view(), name='vendor_update'),
    path('dashboard/', VendorProfile.as_view(), name='vendor_dashboard')
]