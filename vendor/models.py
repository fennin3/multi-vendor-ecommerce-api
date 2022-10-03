from email.policy import default
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from autoslug import AutoSlugField
import uuid







class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email address cannot be left empty!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", 'ADMIN')

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must set is_staff to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must set is_superuser to True"))

        return self.create_user(email, password, **extra_fields)

        

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
      ('VENDOR', 'Vendor'),
      ('CUSTOMER', 'Customer'),
      ('ADMIN', 'Administrator')
    )

    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=15)
    avatar = models.ImageField(upload_to="media/User-Avatar/", default="profile.png")
    is_confirmed = models.BooleanField(_("is confirmed"), default=False)
    confirmation_code = models.IntegerField(
        _("confirmation code"), default=0
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.uid}"


from administrator.models import Country

class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(_("shop name"), blank=False, null=False, max_length=250)
    slug = AutoSlugField(populate_from='shop_name',unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(_("description"))
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=16
    )
    pending_balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    # withdrawal_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    closed = models.BooleanField(default=False)
    suspended = models.BooleanField(default=False)
    banner = models.ImageField(upload_to="media/Shop-Banners/", default='vendor-avatar.default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.slug == "" or self.slug == None:
    #         self.slug = slugify(self.shop_name)
    #     super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.shop_name


class ConfirmationCode(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)





# class Transaction(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     product = models.ForeignKey(Product)
#     price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True,)
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
#     success = models.BooleanField(default=True)
