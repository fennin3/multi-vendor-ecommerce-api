from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from product.models import FlashSale, FlashSaleRequest
from vendor.exceptions import CustomException

from vendor.models import CustomUser
from vendor.serializers import UserSerializer
from vendor.tasks import send_confirmation_mail

from .models import Administrator, Banner, SiteConfiguration, SiteAddress, ShippingFeeZone, Country


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Administrator 
        fields = ("user","phone_number")


    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "ADMINISTRATOR"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        # send_confirmation_mail().delay('Confirm Your Account', user, 'mail.html')
        administrator = Administrator.objects.create(user=user, **validated_data)
        return administrator

class AdminSerializer2(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Administrator 
        fields = ("user","phone_number")

class ConfirmAccountSerializer(serializers.Serializer):
    confirmation_code = serializers.IntegerField(required=True)


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise CustomException({'message':'User account does not exist'})

    
            
        if not user.is_confirmed:
            raise CustomException({'message':'User account has not been confirmed'})

        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)

        '''
        except User.DoesNotExist:
            raise CustomException({'detail':'User account does not exist'})
        '''
        
        return {
            'email':user.email,
            'token': jwt_token
        }

class SiteAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAddress
        fields="__all__"

class SiteConfigSerializer(serializers.ModelSerializer):
    addresses = SiteAddressSerializer(many=True, read_only=True)
    class Meta:
        model=SiteConfiguration
        exclude=('id',)

class SiteConfigSerializer(serializers.ModelSerializer):
    addresses = SiteAddressSerializer(many=True, read_only=True)
    phone_number = serializers.CharField(required=False)
    site_email = serializers.EmailField(required=False)
    note = serializers.CharField(required=False)
    
    class Meta:
        model=SiteConfiguration
        exclude=('id',)


class ApproveDealOfTheDay(serializers.Serializer):
    product = serializers.UUIDField()
    overwrite = serializers.BooleanField(default=False)
    # note = serializers.CharField(max_length=1000000, required=False)

class DeclineDealOfTheDay(serializers.Serializer):
    deal_request = serializers.UUIDField()
    note = serializers.CharField(max_length=1000000, required=False)


class SuspendVendorSerializer(serializers.Serializer):
    uid = serializers.UUIDField()

class UpdateOrderStatusSerializer(serializers.Serializer):
    order_uid = serializers.UUIDField()
    status = serializers.CharField(max_length=255)


class ShippingFeeZoneSerializer(serializers.ModelSerializer):
    shipping_fee = serializers.DecimalField(max_digits=9, decimal_places=2,)
    class Meta:
        model=ShippingFeeZone
        fields="__all__"

class CountrySerializer(serializers.ModelSerializer):
    shipping_zones = ShippingFeeZoneSerializer(read_only=True, many=True)
    # states = StateSerializer(read_only=True)
    class Meta:
        model=Country
        fields="__all__"

class CountrySerializer2(serializers.ModelSerializer):
    shipping_zones = serializers.ListField(child=serializers.CharField(),required=True)
    class Meta:
        model=Country
        fields="__all__"


class CountrySerializer3(serializers.ModelSerializer):
    shipping_zones = serializers.ListField(child=serializers.CharField(),required=False)
    code = serializers.CharField(max_length=4, required=False)
    tel = serializers.CharField(max_length=4, required=False)
    class Meta:
        model=Country
        fields="__all__"


class FlashSaleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashSaleRequest
        fields="__all__"

class FlashSaleRequestSerializer2(serializers.ModelSerializer):
    class Meta:
        model = FlashSaleRequest
        fields="__all__"

        extra_kwargs = {
            "is_approved":{"read_only":True}
        }


class AddFlashSaleSerializer(serializers.Serializer):
    product = serializers.UUIDField(required=True)
    # end_date = serializers.DateTimeField(required=True,format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model=FlashSale
        fields="__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields="__all__"

class BannerSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields="__all__"

    extra_kwargs ={
        "is_active":{"read_ony":True}
    }


