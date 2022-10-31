from rest_framework import serializers
from .models import PaymentMethods
from vendor.serializers import UserSerializer

class PaymentMethodSerializer(serializers.ModelSerializer):
    verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = PaymentMethods
        fields="__all__"

        extra_kwargs = {
            "is_active":{"default":True}
        }


class PaymentMethodSerializer2(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = PaymentMethods
        fields="__all__"

        extra_kwargs = {
            "is_active":{"default":True}
        }