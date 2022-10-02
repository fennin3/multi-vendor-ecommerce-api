from django.contrib import admin
from .models import Country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name','id','is_active')


admin.site.register(Country,CountryAdmin)