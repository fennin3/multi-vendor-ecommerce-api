from django.contrib import admin
from .models import FlashSaleRequest, SubCategory, Product, Image, Color, Review, Size, ProductVariation, Category,DealOfTheDay, FlashSale

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","uid")

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ("uid",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("uid","rate","created_at")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","uid")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","uid")

admin.site.register(SubCategory, CategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Size)
admin.site.register(DealOfTheDay)
admin.site.register(Color)
admin.site.register(FlashSale)
admin.site.register(FlashSaleRequest)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
