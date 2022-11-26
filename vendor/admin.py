from django.contrib import admin

from .models import CustomUser, Vendor, ConfirmationCode, DealOfTheDayRequest

class VendorAdmin(admin.ModelAdmin):
    list_display = ("shop_name","user")

    @admin.display(description="USER")
    def get_user_avatar(self,obj):
        return obj.user

admin.site.register(CustomUser)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(ConfirmationCode)
admin.site.register(DealOfTheDayRequest)
