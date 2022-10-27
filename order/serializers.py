from rest_framework import serializers
from .models import Order,OrderItem
from customer.serializers import CustomerSerializer
# from vendor.serializers import VendorSerializer
from product.serializers import ColorSerializer, ProductSerializer3, SizeSerializer

class AddToCartSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    size = serializers.CharField(max_length=10)
    color = serializers.CharField(max_length=10)



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
class MonthSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    # status = serializers.CharField(max_length=10)

class AnnualSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    # status = serializers.CharField(max_length=10)
