from django.urls import path
from . import views


urlpatterns = [
    path('bank/', views.ListPaymentMethod.as_view(), name="add_list_bank"),
    path('bank-detail/<uid>/', views.UpdatePaymentMethod.as_view(), name="update_bank"),
]
