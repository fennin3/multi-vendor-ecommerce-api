from email.policy import default
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from vendor.models import CustomUser

class Administrator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )

    def __str__(self):
        return f"{self.user.email} - {self.user.uid}"


class Country(models.Model):
    # uid = models.UUIDField(default=uuid.uuid4, editable=False,)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4)
    tel = models.CharField(max_length=4)
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




    
