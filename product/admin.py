from django.contrib import admin
from .models import Category, Product, Image, Color, Review, Size, ProductVariation

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","uid")

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ("uid",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("uid","rate","created_at")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)

