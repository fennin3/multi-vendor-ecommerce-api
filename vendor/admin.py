from django.contrib import admin

from .models import CustomUser, Vendor, ConfirmationCode

class VendorAdmin(admin.ModelAdmin):
    list_display = ("shop_name","user")

admin.site.register(CustomUser)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(ConfirmationCode)
