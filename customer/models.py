from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from administrator.models import Country
from vendor.models import CustomUser

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.TextField(_("address"), null=True, blank=True)
    phone_number = models.CharField(_("phone number"), blank=False, null=False, max_length=16)
    is_active = models.BooleanField(default=True)
    suspended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # avatar = models.ImageField(upload_to="media/Customer-Avatar/", default="profile.png")

    def __str__(self):
        return self.user.email

        
