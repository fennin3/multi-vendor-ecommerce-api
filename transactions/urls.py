from django.urls import path
from . import views


urlpatterns = [
    path('add-bank/', views.AddPaymentMethod.as_view(), name="add_bank"),
    path('bank-detail/<uid>/', views.RetrievePaymentMethod.as_view(), name="retrieve_bank"),
    path('bank-update/<uid>/', views.UpdatePaymentMethod.as_view(), name="update_bank"),
]
