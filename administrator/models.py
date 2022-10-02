import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from vendor.models import CustomUser

class Administrator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )

    def __str__(self):
        return self.user.email


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

    
