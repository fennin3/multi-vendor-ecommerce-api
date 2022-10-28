from administrator.models import Testimonial
from product.serializers import ProductSerializer
from vendor.exceptions import CustomException
from vendor.models import ConfirmationCode, CustomUser
from vendor.tasks import send_confirmation_mail
from vendor.serializers import UserSerializer


from rest_framework import serializers, status
# from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from vendor.utils import gen_confirmation_code

from .models import ContactMessage, Customer, NewsLetterSubscriber, WishItem
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class CustomerSerializer2(serializers.ModelSerializer):
    country = serializers.UUIDField(required=False)
    city = serializers.CharField(max_length=255,required=False)
    phone_number = serializers.CharField(max_length=16, required=False)
    class Meta:
        model=Customer
        fields = ("address","country", "city", "phone_number")

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ("user", "address","country", "city", "phone_number")

class CustomerSerializer2(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Customer
        fields = ("address","country", "city", "phone_number")

        extra_kwargs = {
            "country":{"required":False}, 
            "address":{"required":False}, 
            "city":{"required":False}, 
            "phone_number":{"required":False}, 
        }


    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "CUSTOMER"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        cc = ConfirmationCode.objects.create(code=gen_confirmation_code(), user=user)
        # send_confirmation_mail().delay('Confirm Your Account', user, cc.code)
        new_user = {'first_name':user.first_name, 'email':user.email}
        send_confirmation_mail('Confirm Your Account', new_user, cc.code)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class ConfirmAccountSerializer(serializers.Serializer):
    confirmation_code = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise CustomException({'detail':'User account does not exist'})

    
            
        if not user.is_confirmed:
            raise CustomException({'detail':'User account has not been confirmed'})
        elif not user.user_type == 'CUSTOMER':
            raise CustomException({'detail':"You are not authorized as a customer"}, status_code=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)

        '''
        except User.DoesNotExist:
            raise CustomException({'detail':'User account does not exist'})
        '''
        
        return {
            'email':user.email,
            'token': str(refresh.access_token) + "||" + str(refresh)
        }

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactMessage
        fields="__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Testimonial
        fields="__all__"

class WishItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=WishItem
        fields="__all__" 


class WishItemSerializer2(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model=WishItem
        fields="__all__" 

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsLetterSubscriber
        fields="__all__"