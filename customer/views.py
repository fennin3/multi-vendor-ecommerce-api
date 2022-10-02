#API VIews
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from vendor.models import ConfirmationCode, CustomUser, Vendor

from .models import Customer
from .permissions import IsCustomer
from .serializers import CustomerSerializer, UserLoginSerializer, ConfirmAccountSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# List and Create customers
class CreateCustomer(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Get details of a vendor
class CustomerProfile(generics.RetrieveAPIView):
    permission_classes = (IsCustomer,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        data = CustomerSerializer(customer).data
        return Response(data, status=status.HTTP_200_OK)

# Confirm user account
class ConfirmAccount(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

    # Handle cases where confirmation code is not attached to an account
        user = get_object_or_404(User, email=serializer.data['email'])
        try:
            code = ConfirmationCode.objects.get(
                code=serializer.data["confirmation_code"],
                user=user
            )
            code.delete()
            # handle cases where account is already confirmed
            if user.is_confirmed:
                return Response(
                    {"message": "User account already confirmed!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # confirm account
            user.is_confirmed = True
            user.active = True
            user.save()

            # open shop
            if user.user_type == 'VENDOR':
                vendor = get_object_or_404(Vendor, user=user)
                vendor.closed = False
                vendor.save()

            return Response(
                {"message": "Account confirmed successfully!"}, status=status.HTTP_200_OK
            )
        except ConfirmationCode.DoesNotExist:
            return Response(
                {"message": "incorrect confirmation code"},
                status=status.HTTP_400_BAD_REQUEST,
            )


#Login User
class CustomerLogin(CreateAPIView):
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

  
