from django.contrib import admin

from .models import Customer, ContactMessage, WishItem


admin.site.register(Customer)
admin.site.register(ContactMessage)
admin.site.register(WishItem)