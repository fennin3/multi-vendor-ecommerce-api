#API VIews
from datetime import datetime
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from administrator.models import Banner, Testimonial
from administrator.serializers import BannerSerializer2
from product.models import DealOfTheDay, Product, SubCategory
from product.serializers import CategorySerializer, DealOfTheDaySerializer, ProductSerializer
from vendor.models import ConfirmationCode, Vendor
from vendor.paginations import ClientPagination
from django.db.models import Count
from .models import ContactMessage, Customer, WishItem
from .permissions import IsCustomer
from .serializers import ContactMessageSerializer, CustomerSerializer, CustomerSerializer2, TestimonialSerializer, UserLoginSerializer, ConfirmAccountSerializer, WishItemSerializer, WishItemSerializer2
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

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


# Update details of a vendor
class CustomerProfileUpdate(generics.UpdateAPIView):
    permission_classes = (IsCustomer,)
    serializer_class = CustomerSerializer2
    queryset = Customer.objects.all()
    lookup_field = "user__uid"

    def patch(self, request):
        customer = get_object_or_404(Customer, user=request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.update(customer,serializer.validated_data)

        return Response(self.serializer_class(data).data, status=status.HTTP_200_OK)

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

  
class RetrieveDealOfTheDay(APIView):
    permission_classes= (AllowAny,)
    serializer_class = DealOfTheDaySerializer


    def get(self, request):
        deals = DealOfTheDay.objects.select_related('product').filter(is_active=True, end_date__gte=datetime.now()).order_by('-start_date')

        if deals.exists():
            deal = deals[0]
            data = self.serializer_class(deal).data
            return Response({
                "deal":data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "deal":None
            }, status=status.HTTP_200_OK)

class RetrieveFeaturedProducts(generics.ListAPIView):
    permission_classes=()
    serializer_class = ProductSerializer
    pagination_class = ClientPagination
    queryset = Product.objects.filter(is_active=True,is_approved=True, vendor__suspended=False, vendor__closed=False, featured=True, category__is_active=True, sub_categories__is_active=True).order_by("-created_at")
    
class PopularProducts(generics.ListAPIView):
    permission_classes=()
    serializer_class = ProductSerializer
    pagination_class = ClientPagination
    queryset = Product.objects.filter(product_items__ordered=True).annotate(count=Count("product_items")).filter(is_active=True,is_approved=True, 
    vendor__suspended=False, vendor__closed=False, 
    category__is_active=True, sub_categories__is_active=True).order_by("-count")
    

class RecentProducts(generics.ListAPIView):
    permission_classes=(AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = ClientPagination
    
    queryset = Product.objects.filter(
        is_active=True,
        is_approved=True, 
        vendor__suspended=False, 
        vendor__closed=False, 
        category__is_active=True, 
        sub_categories__is_active=True).order_by("-created_at")

# class PopularSubCategories(generics.ListAPIView):
#     permission_classes=(AllowAny,)
#     serializer_class = CategorySerializer
#     pagination_class = ClientPagination
#     queryset = SubCategory.objects.filter(is_active=True).annotate(count=Count("product_items")).filter(is_active=True,is_approved=True, 
#     vendor__suspended=False, vendor__closed=False, 
#     category__is_active=True, sub_categories__is_active=True).order_by("-count")


class RetrieveAllBanners(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BannerSerializer2
    

    def get(self,request):
        queryset = Banner.objects.filter(is_active=True)
        serializer = self.serializer_class(queryset, many=True)

        return Response(
            {
                "banners":serializer.data
            }, status=status.HTTP_200_OK
        )


class ContactMessageView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()


class ListTestimonials(generics.ListAPIView):
    permission_classes =()
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    pagination_class = ClientPagination

class WishListViews(generics.ListCreateAPIView):
    permission_classes = (IsCustomer,)
    serializer_class = WishItemSerializer
    queryset = WishItem.objects.all()

    def get(self, request):
        wishitems = self.queryset.filter(user=request.user)

        page = self.paginate_queryset(wishitems)
        if page is not None:
            serializer = WishItemSerializer2(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = WishItemSerializer2(wishitems, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class WishListRetrieveDeleteViews(generics.RetrieveDestroyAPIView):
    permission_classes = (IsCustomer,)
    serializer_class = WishItemSerializer
    queryset = WishItem.objects.all()
    lookup_field = "uid"


