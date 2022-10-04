from django.urls import path

from .views import AddSiteAddress, ListandCreateAdmin, AdminLogin, UpdateAddress



urlpatterns = [
    path('', ListandCreateAdmin.as_view(), name='list_and_create_admin'),
    path('signin/', AdminLogin.as_view(), name='admin_login'),
    path('add-address/', AddSiteAddress.as_view(), name='add_address'),
    path('add-address/<pk>/', UpdateAddress.as_view(), name='add_address'),
    path('update-address/', UpdateAddress.as_view(), name='update_address'),
]