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
    is_active = models.BooleanField(default=True)

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
    shipping_zones = models.ManyToManyField(ShippingFeeZone, related_name="countries", blank=True)
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

class SocialMedia(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=255, default="")
    handle = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.handle    

class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    maintenance_mode = models.BooleanField(default=False)
    phone_number = models.TextField(null=False, blank=True)
    site_email = models.EmailField(null=False, blank=True)
    appstore_link = models.URLField(blank=True)
    playstore_link = models.URLField(blank=True)
    note = models.TextField(null=False, blank=True)
    working_hours = models.TextField(blank=True, null=True)
    addresses = models.ManyToManyField(SiteAddress,blank=True)
    # social_media = models.ManyToManyField(SocialMedia,blank=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"

    def socials(self):
        socials = SocialMedia.objects.filter(is_active=True)
        return socials


class Banner(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000)
    header = models.CharField(max_length=1000)
    sub_header = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="media/Banners/")
    btn_link = models.CharField(max_length=1000)
    btn_text = models.CharField(max_length=1000)
    btn_color = models.CharField(max_length=255)
    btn_text_color = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Testimonial(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=1000)
    caption = models.CharField(max_length=1000)
    body = models.TextField()
    avatar = models.ImageField(upload_to="media/Testimonial/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    


class Visitor(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=255)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} -   visited site at   -   {self.visited_at}"


