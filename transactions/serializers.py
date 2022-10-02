from rest_framework import serializers
from .models import PaymentMethods

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields="__all__"