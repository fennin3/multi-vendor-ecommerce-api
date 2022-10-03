from django.shortcuts import get_object_or_404
from rest_framework import serializers

from vendor.models import Vendor
from vendor.serializers import UserSerializer, VendorSerializer

from .models import Color, Product, Image, Category, ProductVariation, Review, Size


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name","slug")

        extra_kwargs = {
            "slug": {'validators': []},
            "closed": {"slug": True},
        }

    

class ImageSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    class Meta:
        model = Image
        fields = ("uid","image",)


class ProductSerializer2(serializers.ModelSerializer):
    categories = serializers.ListField(child=serializers.CharField())
    thumbnail = serializers.ImageField()
    images = serializers.ListField(child=serializers.ImageField(), required=False, allow_null=True)
    sizes = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    colors = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    
    class Meta:
        model = Product
        fields = ("name", "categories", "price", "stock","description","images", "discount_type","discount", "thumbnail", "sizes", "colors")

        extra_kwargs = {
            "slug": {"read_only": True},
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

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model=Review
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    uid = serializers.UUIDField(read_only=True)
    colors = ColorSerializer(read_only=True, many=True)
    sizes = SizeSerializer(read_only=True, many=True)
    variants = VariantSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    
    class Meta:
        model = Product
        fields = ("uid", "slug","name", "categories", "price", "stock","description","images", "discount_type","discount", "thumbnail","sizes", "colors", "variants", "is_active", "is_approved", "reviews")


class ProductSerializer3(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    uid = serializers.UUIDField(read_only=True)
    # colors = ColorSerializer(read_only=True, many=True)
    # sizes = SizeSerializer(read_only=True, many=True)
    # variants = VariantSerializer(read_only=True, many=True)
    
    class Meta:
        model = Product
        fields = ("uid", "slug","name", "categories", "price", "stock","description","images", "is_active", "is_approved")



        






