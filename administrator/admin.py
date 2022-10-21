from django.contrib import admin
from .models import Country, SiteConfiguration, Administrator, SiteAddress, ShippingFeeZone, Banner
from solo.admin import SingletonModelAdmin


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name','uid','is_active')

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(SiteAddress)
admin.site.register(Banner)
admin.site.register(Administrator)
admin.site.register(ShippingFeeZone)