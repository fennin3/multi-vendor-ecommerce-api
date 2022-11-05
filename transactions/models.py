import uuid
from django.db import models
from administrator.models import Country

from vendor.models import CustomUser


class PaymentMethods(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    bank_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=25)
    account_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="payment_details", null=True, blank=True)


    def __str__(self):
        return self.account_no

    
# class Transaction(models.Model):
#     pass
    
class SaleIncome(models.Model):
    INCOME_FOR = (
        ("admin","admin"),
        ("vendor","vendor"),
    )
    STATUS = (
        ("pending","pending"),
        ("paid","paid"),
        ("refunded","refunded")
    )
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    income_for = models.CharField(max_length=8,choices=INCOME_FOR)
    user = models.UUIDField(null=True, blank=True)
    transaction_ref = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=9,decimal_places=2)
    status = models.CharField(max_length=10, default="pending", choices=STATUS)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)