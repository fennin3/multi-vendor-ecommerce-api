from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from administrator.views import CountVisitor, ListCountries, GetSiteInfo, PrivacyPolicy, TermsNConditions,UpdateSiteInfo
from customer.views import ContactMessageView, ListShippingZonesView, ListTestimonials, SubscribeNewsLetter, VerifyNewsLetterEmail
from product.views import AllCatgories, AllSubCatgories, CategoryProducts, CategorySubCategory, ListColors, ListSizes, RetrieveCategoryDetail, RetrieveSubCatgoryDetail, SubCategoryProducts
from vendor.views import CustomUserDetail, Logout

from rest_framework_jwt.blacklist.views import BlacklistView
from rest_framework_jwt.views import refresh_jwt_token


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

    # Category
    path("category/<uid>/subcategories/", CategorySubCategory.as_view(), name="cat_subcat"),
    path("categories/", AllCatgories.as_view(), name="all_cats"),
    path("categories/<uid>/", RetrieveCategoryDetail.as_view(), name="cat_detail"),
    path("subcategories/", AllSubCatgories.as_view(), name="all_subcats"),
    path("subcategories/<uid>/", RetrieveSubCatgoryDetail.as_view(), name="subcat_detail"),
    path("category/<uid>/products/", CategoryProducts.as_view(), name="cat_prods"),
    path("subcategory/<uid>/products/", SubCategoryProducts.as_view(), name="cat_prods"),

    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy_policy"),
    path("terms-conditions/", TermsNConditions.as_view(), name="terms"),

    path("contact-us/", ContactMessageView.as_view(), name="contact_us"),

    path("testimonials/", ListTestimonials.as_view(), name="testimonials"),

    path("auth/logout/", BlacklistView.as_view({"post": "create"})),

    path("auth/logout/", Logout.as_view(), name="logout"),

    path('auth/token-refresh/', refresh_jwt_token, name="refresh_token"),

    path('visitors/count/', CountVisitor.as_view(), name='count_visitors'),

    path("colors/", ListColors.as_view(), name="colors"),
    path("sizes/", ListSizes.as_view(), name="sizes"),
    path("zones/", ListShippingZonesView.as_view(), name="zones"),

    path("newsletter/subscribe/", SubscribeNewsLetter.as_view(), name="subscribe"),
    path("newsletter/verify/<ciphertext>/", VerifyNewsLetterEmail.as_view(), name="subscriber_verify"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)