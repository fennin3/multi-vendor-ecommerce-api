from email.policy import default
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from administrator.models import Country
from product.models import Product
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


class ContactMessage(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.full_name}"


class WishItem(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"WishItem for {self.user}"

class NewsLetterSubscriber(models.Model):
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural="Subscribers"
    
    
    

        
