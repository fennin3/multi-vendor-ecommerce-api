from django.contrib import admin

from .models import Customer, ContactMessage, NewsLetterSubscriber, WishItem

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user",]


admin.site.register(Customer,CustomerAdmin)
admin.site.register(ContactMessage)
admin.site.register(WishItem)
admin.site.register(NewsLetterSubscriber)