from django.urls import path

from customer.views import PopularProducts, RecentProducts, RetrieveFeaturedProducts

from .views import (AddProductVariant, CreateListProduct, DeleteProductImage,
 ImageUploadView, CategoryView, ListAllProducts, ListVendorProduct, ProductReviewsVendor, UpdateProductStatus, UpdateRetrieveDestroyProductVariant,
  UpdateRetrieveDetroyProduct, VariantStatus)


urlpatterns = [
    path('', ListAllProducts.as_view(), name='list_products'),
    path('featured/', RetrieveFeaturedProducts.as_view(), name="list_featured"),
    path('popular/', PopularProducts.as_view(), name="list_popular"),
    path('recent/', RecentProducts.as_view(), name="list_recent"),
    path('create/', CreateListProduct.as_view(), name='create_list_products'),
    path('add-variant/', AddProductVariant.as_view(), name="add_variant"),
    path('variants/<uid>/', UpdateRetrieveDestroyProductVariant.as_view(), name="add_variant"),
    path('variant-status/<uid>/', VariantStatus.as_view(), name="variant_status"),
    path('vendors/<vendor_id>/', ListVendorProduct.as_view(), name='get_vendor_products'),
    path('vendor/reviews/', ProductReviewsVendor.as_view(), name='get_vendor_reviews'),
    path('<uid>/', UpdateRetrieveDetroyProduct.as_view(), name='update_products'),
    path('<uid>/image/', ImageUploadView.as_view(), name='upload_image'),
    path('image-delete/<uid>/', DeleteProductImage.as_view(), name='delete_image'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('update-status/<uid>/', UpdateProductStatus.as_view(), name="update_prod_status"),

]
