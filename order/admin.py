from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

class ShippinAddressAdmin(admin.ModelAdmin):
    list_display = ("uid","recipient_name",)


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress,ShippinAddressAdmin)