from administrator.models import Testimonial
from product.serializers import ProductSerializer
from vendor.exceptions import CustomException
from vendor.models import ConfirmationCode, CustomUser
from vendor.tasks import send_confirmation_mail
from vendor.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist



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


# class CustomerSerializer2(serializers.ModelSerializer):
#     country = serializers.UUIDField(required=False)
#     city = serializers.CharField(max_length=255,required=False)
#     phone_number = serializers.CharField(max_length=16, required=False)
#     class Meta:
#         model=Customer
#         fields = ("address","country", "city", "phone_number")

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
        

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    email = serializers.EmailField(write_only=True, source="user__email")
    first_name = serializers.CharField(write_only=True, source="user__first_name")
    last_name = serializers.CharField(write_only=True, source="user__last_name")
    password = serializers.CharField(write_only=True,source="user__password")
    avatar = serializers.ImageField(required=False, allow_null=False,write_only=True, source="user__avatar")
    user_type = serializers.CharField(default="", required=False, write_only=True, source="user__user_type")
    class Meta:
        model = Customer
        fields = ("user","email","first_name","last_name","password","avatar","user_type", "address","country", "city", "phone_number")


    def create(self, validated_data):
        user_data = {}
        user_data['email'] = validated_data.pop("user__email")
        user_data['first_name'] = validated_data.pop("user__first_name")
        user_data['last_name'] = validated_data.pop("user__last_name")
        user_data['password'] = validated_data.pop("user__password")
        user_data['user_type'] = validated_data.pop("user__user_type")
        user_data.update({"user_type": "CUSTOMER"})

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