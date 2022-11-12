from django.contrib import admin
from .models import PaymentMethods, SaleIncome

admin.site.register(PaymentMethods)
admin.site.register(SaleIncome)