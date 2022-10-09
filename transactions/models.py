from email.policy import default
import uuid
from django.db import models

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
    
