from email.policy import default
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from vendor.models import CustomUser

class Administrator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=16
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.email} - {self.user.uid}"


class ShippingFeeZone(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    shipping_fee = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

# class State(models.Model):
#     uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     shipping_fee = models.ForeignKey(ShippingFeeZone,on_delete=models.PROTECT,related_name="states", null=True, blank=True)

#     def __str__(self):
#         return self.name


class Country(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4)
    tel = models.CharField(max_length=4)
    # has_states = models.BooleanField(default=False)
    # shipping_fee = models.ForeignKey(ShippingFeeZone,on_delete=models.PROTECT,related_name="countries", null=True, blank=True)
    shipping_zones = models.ManyToManyField(ShippingFeeZone, related_name="countries")
    is_active = models.BooleanField(default=True)

    class Meta:
            verbose_name_plural = "Countries"


    def __str__(self):
        return self.name



class SiteAddress(models.Model):
    title = models.CharField(max_length=10000)
    email = models.EmailField()
    phone_number = models.TextField()
    location = models.TextField()
    coordinates = models.JSONField()
    image = models.ImageField(upload_to="media/Site-Addresses/")

    def __str__(self):
        return self.title
    

class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    maintenance_mode = models.BooleanField(default=False)
    phone_number = models.TextField()
    site_email = models.EmailField()
    note = models.TextField()
    addresses = models.ManyToManyField(SiteAddress,blank=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"




    
