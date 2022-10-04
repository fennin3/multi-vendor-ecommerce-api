from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from vendor.exceptions import CustomException

from vendor.models import CustomUser
from vendor.serializers import UserSerializer
from vendor.tasks import send_confirmation_mail

from .models import Administrator, SiteConfiguration, SiteAddress


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
        send_confirmation_mail().delay('Confirm Your Account', user, 'mail.html')
        administrator = Administrator.objects.create(user=user, **validated_data)
        return administrator

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


# class 