#API VIews
import uuid
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from administrator.permissions import IsSuperuser
from administrator.serializers import FlashSaleRequestSerializer2
from rest_framework_jwt.blacklist.models import BlacklistedToken

# from administrator.permissions import IsSuperuser
from order.models import OrderItem

from product.models import FlashSaleRequest, Product
from vendor.paginations import AdminVendorPagination, ClientPagination

from .models import ConfirmationCode, CustomUser, DealOfTheDayRequest, Vendor
from .permissions import IsUser, IsVendor
from .serializers import DealOfTheDayRequestSerializer, UpdateOrderStatusSerializer, UserSerializer, VendorSerializer, ConfirmAccountSerializer, UserLoginSerializer, VendorSerializer2, VendorSerializer3

from order.serializers import OrderItemSerializer

from rest_framework.generics import UpdateAPIView
from datetime import date, datetime, timedelta





# List and Create vendors
class VendorList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Vendor.objects.all().order_by('-created_at')
    serializer_class = VendorSerializer

# Get details of a vendor
class VendorDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer2
    lookup_field = 'user__uid'

# Confirm user account
class ConfirmAccount(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Handle cases where confirmation code is not attached to an account
        user = get_object_or_404(CustomUser, email=serializer.data['email'])
        try:
                # user = CustomUser.objects.get(
                #     confirmation_code=serializer.data["confirmation_code"]
                # )
                        # handle cases where account is already confirmed
            
            code = ConfirmationCode.objects.get(
                code=serializer.data["confirmation_code"],
                user=user
            )
            code.delete()
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
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "incorrect confirmation code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

#Login User
class VendorLogin(APIView):
    permission_classes =()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = CustomUser.objects.get(email=serializer.data['email']).uid
        response = {
            'success' : 'True',
            'status_code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'uid':uid,
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class VendorUpdate(UpdateAPIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer3
    lookup_field = "user__uid"

class VendorProfile(RetrieveAPIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        print(request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
        data = VendorSerializer(vendor).data
        return Response(data, status=status.HTTP_200_OK)

class VendorCloseOrOpen(APIView):
    permission_classes = (IsVendor,)
    
    def patch(self, request):
        vendor = Vendor.objects.select_related('user').get(user=request.user)
        vendor.closed = not vendor.closed
        print(vendor)
        vendor.save()
        val = "Closed" if vendor.closed else "Opened"
        return Response(
            {
                "message":f"Your is {val}"
            },status=status.HTTP_200_OK
        )

class CreateDealOfTheRequestView(generics.ListCreateAPIView):
    queryset = DealOfTheDayRequest.objects.select_related('vendor','product').all()
    serializer_class = DealOfTheDayRequestSerializer
    permission_classes=(IsSuperuser,)
    pagination_class = AdminVendorPagination

    def get(self, request):
        queryset = self.queryset.filter(vendor__user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class DeleteUpdateRetrieveDealOfTheRequestView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealOfTheDayRequest.objects.select_related('vendor','product').all()
    serializer_class = DealOfTheDayRequestSerializer
    permission_classes=(IsSuperuser,)
    lookup_field = "uid"


class CustomUserDetail(generics.UpdateAPIView):
    permission_classes = (IsUser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "uid"        


class FeaturedVendors(generics.ListAPIView):
    permission_classes=(AllowAny,)
    serializer_class = VendorSerializer
    pagination_class=ClientPagination
    queryset = Vendor.objects.filter(suspended=False, closed=False, featured=True)


class ListCreateFlashRequest(generics.ListCreateAPIView):
    permission_classes = (IsVendor,)
    serializer_class = FlashSaleRequestSerializer2
    pagination_class=ClientPagination
    queryset = FlashSaleRequest.objects.all()

    def get(self, request):
        flash_sales = self.queryset.filter(product__vendor__user=request.user)

        page = self.paginate_queryset(flash_sales)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(flash_sales, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class Logout(APIView):
    def post(self, request):
        token = str(request.headers.get("Authorization")).split(" ")[1]

        blcklst = BlacklistedToken.objects.create(
            user = request.user,
            token = token,
            token_id = uuid.uuid4(),
            expires_at = datetime.now() + timedelta(days=1)
        )

        return Response(
            {"message":"logged out successfully"}, status=status.HTTP_200_OK
        )


class TokenRefresh(APIView):
    def post(self, request):
        token = str(request.headers.get("Authorization")).split(" ")[1]

        blcklst = BlacklistedToken.objects.create(
            user = request.user,
            token = token,
            token_id = uuid.uuid4(),
            expires_at = datetime.now() + timedelta(days=1)
        )

        return Response(
            {"message":"logged out successfully"}, status=status.HTTP_200_OK
        )


