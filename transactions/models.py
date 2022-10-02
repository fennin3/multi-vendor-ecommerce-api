from django.db import models


class PaymentMethods(models.Model):
    uid = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=25)
    account_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.account_no
    
