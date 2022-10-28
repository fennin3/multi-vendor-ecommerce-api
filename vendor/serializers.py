from vendor.utils import gen_confirmation_code
from .exceptions import CustomException
from .models import CustomUser, DealOfTheDayRequest, Vendor, ConfirmationCode
from .tasks import send_confirmation_mail

from rest_framework import serializers, status
from rest_framework_jwt.settings import api_settings




from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login



from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "uid",
            "email",
            "first_name",
            "last_name",
            "password",
            "user_type",
            "avatar",
            "is_confirmed",
            "date_joined",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
            "is_confirmed": {"read_only": True},
            "user_type": {"read_only": True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


from administrator.models import Country
from administrator.serializers import ShippingFeeZoneSerializer


class CountrySerializer(serializers.ModelSerializer):
    shipping_zones = ShippingFeeZoneSerializer(read_only=True, many=True)
    class Meta:
        model=Country
        fields="__all__"

class VendorSerializer2(serializers.ModelSerializer):
    user = UserSerializer()
    country = CountrySerializer()

    class Meta:
        model = Vendor
        fields = ("user", "shop_name",'country','address', "description", "phone_number","pending_balance","balance", "closed", "suspended", 'banner')

        extra_kwargs = {
            "closed": {"read_only": True},
            "suspended": {"read_only": True},
            "pending_balance": {"read_only": True},
            "balance": {"read_only": True},
        }
        lookup_field = 'user__uid'

class VendorSerializer3(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Vendor
        fields = ("shop_name",'country','address', "description", "phone_number","pending_balance","balance", "closed", "suspended", 'banner')

        extra_kwargs = {
            "closed": {"read_only": True},
            "suspended": {"read_only": True},
            "pending_balance": {"read_only": True},
            "balance": {"read_only": True},
        }


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # country = serializers.UUIDField(required=True, allow_null=False)

    class Meta:
        model = Vendor
        fields = ("user", "shop_name",'country','address', "description", "phone_number","pending_balance","balance", "closed", "suspended", 'banner')

        extra_kwargs = {
            "closed": {"read_only": True},
            "suspended": {"read_only": True},
            "pending_balance": {"read_only": True},
            "balance": {"read_only": True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "VENDOR"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        

        new_user = {'first_name':user.first_name, 'email':user.email}
        
        cc = ConfirmationCode.objects.create(code=gen_confirmation_code(), user=user)
        # send_confirmation_mail.delay('Confirm Your Account', new_user, cc.code)
        send_confirmation_mail('Confirm Your Account', new_user, cc.code)
        print("Email Sent")
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor
        


class ConfirmAccountSerializer(serializers.Serializer):
    confirmation_code = serializers.IntegerField(required=True)
    email = serializers.EmailField()


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
        elif not user.user_type == 'VENDOR':
            raise CustomException({'message':"You are not authorized as a vendor "}, status_code=status.HTTP_401_UNAUTHORIZED)

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

class UpdateOrderStatusSerializer(serializers.Serializer):
    uid = serializers.UUIDField()


class DealOfTheDayRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=DealOfTheDayRequest
        fields="__all__"

        extra_kwargs = {
            "approved":{"read_only":True},
            "deal_date":{"read_only":True},
            "status":{"read_only":True},
        }

