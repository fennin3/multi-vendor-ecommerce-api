from django.urls import path

from product.views import RetrieveFlashSale

from .views import ConfirmAccount, CustomerLogin, CustomerProfileUpdate, RetrieveAllBanners, RetrieveDealOfTheDay, WishListRetrieveDeleteViews, WishListViews

from .views import CreateCustomer, CustomerProfile


urlpatterns = [
    path('', CreateCustomer.as_view(), name='all_vendors'),
    path('profile/', CustomerProfile.as_view(), name='customer_dashboard'),
    path('profile/update/', CustomerProfileUpdate.as_view(), name='customer_dashboard'),
    path('confirm-account/', ConfirmAccount.as_view(), name='confirm_account'),
    path('signin/', CustomerLogin.as_view(), name='sign_in'),
    path('deal/', RetrieveDealOfTheDay.as_view(), name='deal'),
    path('flashsales/', RetrieveFlashSale.as_view(), name="flash_sale"),
    path('banners/', RetrieveAllBanners.as_view(), name="banners"),
    
    path('wishlist/', WishListViews.as_view(), name="wishlist"),
    path('wishlist/<uid>/', WishListRetrieveDeleteViews.as_view(), name="wishlist_one"),
]