from rest_framework import serializers

from coupons.serializers import CouponSerializer
from vendor.serializers import CountrySerializer
from .models import Order,OrderItem, ShippingAddress
from customer.serializers import CustomerSerializer
# from vendor.serializers import VendorSerializer
from product.serializers import ColorSerializer, ProductSerializer3, SizeSerializer

class AddToCartSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    size = serializers.CharField(max_length=10)
    color = serializers.CharField(max_length=10)

class RemoveFromCartSerializer(serializers.Serializer):
    uid = serializers.UUIDField()

class AddQuantitySerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    quantity = serializers.IntegerField()



class OrderItemSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only=True)
    item = ProductSerializer3(read_only=True)
    size = SizeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)

    class Meta:
        model=OrderItem
        fields="__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)
    class Meta:
        model=Order
        fields="__all__"

        extra_kwargs ={
            "order_id":{"read_only":True}
        }

class OrderSerializer2(serializers.ModelSerializer):
    # user = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)
    coupon_used = CouponSerializer(read_only=True)
    order_total = serializers.DecimalField(source='get_total',decimal_places=2, max_digits=9)
    class Meta:
        model=Order
        fields="__all__"

        extra_kwargs ={
            "order_id":{"read_only":True}
        }

class MonthSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    # status = serializers.CharField(max_length=10)

class AnnualSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    # status = serializers.CharField(max_length=10)



class ShippingAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields="__all__"

class ShippingAddressListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    class Meta:
        model=ShippingAddress
        fields="__all__"


class AddAddressToCartSerializer(serializers.Serializer):
    address_uid = serializers.UUIDField()