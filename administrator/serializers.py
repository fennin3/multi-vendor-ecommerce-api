import datetime
from rest_framework import serializers
# from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from product.models import FlashSale, FlashSaleRequest
from vendor.exceptions import CustomException

from vendor.models import CustomUser
from vendor.serializers import UserSerializer
from vendor.tasks import send_confirmation_mail
from django.core.exceptions import ObjectDoesNotExist

from .models import Administrator, Banner, SiteConfiguration, SiteAddress, ShippingFeeZone, Country, SocialMedia
from rest_framework_simplejwt.tokens import RefreshToken


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    email = serializers.EmailField(write_only=True, source="user__email")
    first_name = serializers.CharField(write_only=True, source="user__first_name")
    last_name = serializers.CharField(write_only=True, source="user__last_name")
    password = serializers.CharField(write_only=True,source="user__password")
    avatar = serializers.ImageField(required=False, allow_null=False,write_only=True, source="user__avatar")
    user_type = serializers.CharField(default="", required=False, write_only=True, source="user__user_type")


    class Meta:
        model = Administrator 
        fields = ("user","email","first_name","last_name","password","avatar","user_type","phone_number")

        extra_kwargs = {
            "is_active":{"read_only":True}
        }


    def create(self, validated_data):
        user_data = {}

        user_data = {}
        user_data['email'] = validated_data.pop("user__email")
        user_data['first_name'] = validated_data.pop("user__first_name")
        user_data['last_name'] = validated_data.pop("user__last_name")
        user_data['password'] = validated_data.pop("user__password")
        user_data['user_type'] = validated_data.pop("user__user_type")
        user_data.update({"user_type": "ADMINISTRATOR"})

        try:
            user_data['avatar'] = validated_data.pop("user__avatar")
        except:
            pass

        try:
            CustomUser.objects.get(email=user_data['email'])
            raise serializers.ValidationError({"message":"user with this email address already exists."})

        except ObjectDoesNotExist:
            pass

        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        # send_confirmation_mail().delay('Confirm Your Account', user, 'mail.html')
        administrator = Administrator.objects.create(user=user, **validated_data)
        return administrator

class AdminSerializer2(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True, source="user__email", required=False)
    first_name = serializers.CharField(write_only=True, source="user__first_name", required=False)
    last_name = serializers.CharField(write_only=True, source="user__last_name", required=False)
    # password = serializers.CharField(write_only=True,source="user__password", required=False)
    avatar = serializers.ImageField(required=False, allow_null=False,write_only=True, source="user__avatar")
    
    class Meta:
        model = Administrator 
        fields = ("user","email","first_name","last_name","avatar","phone_number")

        extra_kwargs = {
            "phone_number":{"required":False}, 
        }

    def update(self, instance, validated_data):
        user = instance.user
        user_data = {}
        user_data['email'] = validated_data.get("user__email",user.email)
        user_data['first_name'] = validated_data.get("user__first_name",user.first_name)
        user_data['last_name'] = validated_data.get("user__last_name",user.last_name)
        user_data['avatar'] = validated_data.get("user__avatar",None)

        if user_data["avatar"] == None:
            del user_data["avatar"]
        else:
            del validated_data["user__avatar"]
        
        try:
            validated_data.pop("user__email")
        except:
            pass

        try:
            validated_data.pop("user__first_name")
        except:
            pass

        try:
            validated_data.pop("user__last_name")
        except:
            pass


        user = CustomUser.objects.filter(uid=instance.user.uid).update(**user_data)
        return super().update(instance, validated_data)

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

        refresh = RefreshToken.for_user(user)

        refresh.set_exp(lifetime=datetime.timedelta(seconds=30))

        update_last_login(None, user)

        '''
        except User.DoesNotExist:
            raise CustomException({'detail':'User account does not exist'})
        '''
        
        return {
            'email':user.email,
            'token': str(refresh.access_token) + "||" + str(refresh)
        }

class SiteAddressSerializer(serializers.ModelSerializer):
    # coordinat
    class Meta:
        model = SiteAddress
        fields="__all__"


class SiteAddressSerializer2(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=255,required=False, allow_null=True)
    latitude = serializers.CharField(max_length=255,required=False, allow_null=True)
    coordinates = serializers.JSONField(required=False, allow_null=True)
    class Meta:
        model = SiteAddress
        fields="__all__"

class SiteAddressSerializer3(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=255,required=False, allow_null=True)
    latitude = serializers.CharField(max_length=255,required=False, allow_null=True)
    coordinates = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = SiteAddress
        fields="__all__"

        extra_kwargs = {
            "title":{"required":False,"allow_null":True},
            "email":{"required":False,"allow_null":True},
            "phone_number":{"required":False,"allow_null":True},
            "location":{"required":False,"allow_null":True},
            "image":{"required":False,"allow_null":True}
        }

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model=SocialMedia
        fields="__all__"

        extra_kwargs = {
            "is_active":{"default":True}
        }


# class SiteConfigSerializer(serializers.ModelSerializer):
#     addresses = SiteAddressSerializer(many=True, read_only=True)
#     socials = SocialMediaSerializer(many=True, read_only=True)
#     class Meta:
#         model=SiteConfiguration
#         exclude=('id',)

class SiteConfigSerializer(serializers.ModelSerializer):
    addresses = SiteAddressSerializer(many=True, read_only=True)
    phone_number = serializers.CharField(required=False)
    site_email = serializers.EmailField(required=False)
    note = serializers.CharField(required=False)
    socials = SocialMediaSerializer(many=True, read_only=True)
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

        extra_kwargs = {
            "is_active":{"default":True}
        }

class CountrySerializer(serializers.ModelSerializer):
    shipping_zones = ShippingFeeZoneSerializer(read_only=True, many=True)
    # states = StateSerializer(read_only=True)
    class Meta:
        model=Country
        fields="__all__"
    
        extra_kwargs = {
            "is_active":{"default":True}
        }

class CountrySerializer2(serializers.ModelSerializer):
    shipping_zones = serializers.ListField(child=serializers.CharField(),required=True)
    class Meta:
        model=Country
        fields="__all__"

        extra_kwargs = {
            "is_active":{"default":True}
        }

class CountrySerializer3(serializers.ModelSerializer):
    shipping_zones = serializers.ListField(child=serializers.CharField(),required=False)
    code = serializers.CharField(max_length=4, required=False)
    tel = serializers.CharField(max_length=4, required=False)
    class Meta:
        model=Country
        fields="__all__"


        extra_kwargs = {
            "is_active":{"default":True}
        }


class FlashSaleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashSaleRequest
        fields="__all__"



class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields="__all__"

        extra_kwargs = {
            "is_active":{"default":True}
        }

class BannerSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields="__all__"

    extra_kwargs ={
        "is_active":{"default":True}
    }


