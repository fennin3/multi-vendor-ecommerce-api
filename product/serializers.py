from django.shortcuts import get_object_or_404
from rest_framework import serializers
from administrator.models import Visitor

from vendor.models import Vendor
from vendor.serializers import UserSerializer, VendorSerializer

from .models import Category, Color, DealOfTheDay, FlashSale, Product, Image, SubCategory, ProductVariation, Review, Size


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }

class CategoryUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    category = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = SubCategory
        fields = "__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }

class SubCategorySerializer(serializers.ModelSerializer):
    category = MainCategorySerializer(read_only=True)
    class Meta:
        model = SubCategory
        fields = "__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }

    

class ImageSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    class Meta:
        model = Image
        fields = ("uid","image",)


class ProductSerializer2(serializers.ModelSerializer):
    sub_categories = serializers.ListField(child=serializers.CharField())
    thumbnail = serializers.ImageField()
    images = serializers.ListField(child=serializers.ImageField(), required=True, allow_null=False)
    sizes = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    colors = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    
    class Meta:
        model = Product
        fields = ("name","category", "sub_categories", "price", "stock","description", "additional_info", "images", "discount_type","discount", "thumbnail", "sizes", "colors")

        extra_kwargs = {
            "slug": {"read_only": True},
            "is_active":{"read_only":True}
        }

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields="__all__"

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields="__all__"

class VariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    class Meta:
        model=ProductVariation
        fields = "__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model=Review
        fields="__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }


class ProductSerializer(serializers.ModelSerializer):
    category = MainCategorySerializer(read_only=True)
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    # categories = CategorySerializer(many=True, read_only=True)
    uid = serializers.UUIDField(read_only=True)
    colors = ColorSerializer(read_only=True, many=True)
    sizes = SizeSerializer(read_only=True, many=True)
    variants = VariantSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    vendor = VendorSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ("uid","sku", "slug","name","category", "sub_categories", "price", "stock","description","additional_info","images", "discount_type","discount", "thumbnail", "vendor","sizes", "colors", "variants","rating", "is_active", "is_approved", "reviews","created_at", "updated_at")


class ProductSerializer3(serializers.ModelSerializer):
    category = MainCategorySerializer(read_only=True)
    sub_categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    uid = serializers.UUIDField(read_only=True)
    # colors = ColorSerializer(read_only=True, many=True)
    # sizes = SizeSerializer(read_only=True, many=True)
    # variants = VariantSerializer(read_only=True, many=True)
    
    class Meta:
        model = Product
        fields = ("uid", "slug","name","category", "sub_categories", "price", "stock","description","additional_info","images", "is_active", "is_approved")


class ReviewSerializer2(serializers.ModelSerializer):
    user = UserSerializer()
    product =ProductSerializer3()
    class Meta:
        model=Review
        fields="__all__"


class DealOfTheDaySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=DealOfTheDay
        fields="__all__"

        extra_kwargs = {
            "is_active":{"read_only":True},
            "in_stock":{"read_only":True}
        }

class FlashSaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = FlashSale
        fields="__all__"

        extra_kwargs = {
            "is_active":{"read_only":True}
        }
        

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields="__all__"        





