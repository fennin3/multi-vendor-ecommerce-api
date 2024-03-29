import calendar
from datetime import datetime, timedelta
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from administrator.filters import OrderFilter, ProductFilter
from administrator.tasks import send_deal_request_approval_mail, send_flashsale_approval_mail
from administrator.utils import STATUS
from customer.models import ContactMessage, Customer, NewsLetterSubscriber
from customer.serializers import ContactMessageSerializer, CustomerSerializer, CustomerSerializer2, CustomerSerializer3, SubscriberSerializer, TestimonialSerializer
from order.models import Order
from order.serializers import AnnualSerializer, MonthSerializer, OrderSerializer
from product.filters import CategoryFilter, SubCategoryFilter
from product.models import Category, Color, DealOfTheDay, FlashSale, FlashSaleRequest, Product, Size, SubCategory
from product.serializers import AddFlashSaleSerializer, CategorySerializer, CategoryUpdateSerializer, ColorSerializer, DealOfTheDaySerializer, FlashSaleRequestSerializer3, MainCategorySerializer, ProductSerializer, ProductSerializer2, SizeSerializer, SubCategorySerializer, VisitorSerializer
from transactions.models import PaymentMethods, SaleIncome
from transactions.serializers import PaymentMethodSerializer2
from vendor.models import ConfirmationCode, CustomUser, DealOfTheDayRequest, Vendor
from vendor.paginations import AdminVendorPagination
from vendor.serializers import ConfirmAccountSerializer, DealOfTheDayRequestSerializer, VendorSerializer, VendorSerializer3
from rest_framework.generics import ListAPIView
from .models import Administrator, Banner, Country, ShippingFeeZone, SiteAddress, SiteConfiguration, SocialMedia, Testimonial, Visitor
from .permissions import IsSuperuser
from .serializers import (AdminSerializer, AdminSerializer2, ApproveDealOfTheDay, BannerSerializer, CountrySerializer2,
CountrySerializer, CountrySerializer3, DeclineDealOfTheDay, FlashSaleRequestSerializer, ShippingFeeZoneSerializer, SiteAddressSerializer, SiteAddressSerializer2, SiteAddressSerializer3, SiteConfigSerializer, SocialMediaSerializer,
 SuspendVendorSerializer, UpdateOrderStatusSerializer, UserLoginSerializer)
from django.db.models import Sum,Count
from rest_framework.renderers import TemplateHTMLRenderer
from django_filters import rest_framework as filters
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from vendor.permissions import IsVendor
from djqscsv import render_to_csv_response


# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import logout
# from .resources import ProductResource

class ListandCreateAdmin(generics.ListCreateAPIView):
    permission_classes = (IsSuperuser,)
    queryset = Administrator.objects.all().order_by("-created_at")
    serializer_class = AdminSerializer
    pagination_class = AdminVendorPagination

class AdminLogin(APIView):
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
            'token' : str(serializer.data['token']).split('||')[0],
            'refresh':str(serializer.data['token']).split('||')[1]
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class AdminProfile(generics.RetrieveAPIView):
    permission_classes = (IsSuperuser,)
    # authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        print(request.user)
        admin = get_object_or_404(Administrator, user=request.user)
        data = AdminSerializer(admin).data
        return Response(data, status=status.HTTP_200_OK)


class ListCountries(APIView):
    permission_classes=()
    serializer_class = CountrySerializer

    def get(self, request):
        countries = Country.objects.all().order_by("name")

        serializer = self.serializer_class(countries, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class GetSiteInfo(APIView):
    permission_classes =()
    serializer_class = SiteConfigSerializer

    def get(self,request):
        config = SiteConfiguration.get_solo()
        serializer = self.serializer_class(config)
        return Response(
            serializer.data,status=status.HTTP_200_OK
        )

class UpdateSiteInfo(APIView):
    permission_classes =(IsSuperuser,)
    serializer_class = SiteConfigSerializer
    
    def patch(self, request):
            config = SiteConfiguration.objects.get()
            serializer = self.serializer_class(data=request.data)

            serializer.is_valid(raise_exception=True)

            serializer.update(config,serializer.validated_data)

            return Response(
                {
                    "message":"Configurations has been updated successfully"
                }, status=status.HTTP_200_OK
            )

class AddSiteAddress(APIView):
    permission_classes =(IsSuperuser,)
    serializer_class = SiteAddressSerializer2


    def post(self,request):
        config = SiteConfiguration.objects.get()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['coordinates'] =  {
                "latitude":serializer.data.get('latitude',None),
                "longitude":serializer.data.get('longitude',None)
            }
        data.pop("longitude")
        data.pop("latitude")

        address = serializer.create(data)

        config.addresses.add(address)
        config.save()

        return Response({
            "message":"Address has been saved"
        },status=status.HTTP_200_OK)

class UpdateAddress(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =(IsSuperuser,)
    serializer_class = SiteAddressSerializer
    queryset = SiteAddress.objects.all()

    def partial_update(self, request, pk):
        address = get_object_or_404(SiteAddress,pk=pk)

        serializer = SiteAddressSerializer3(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['coordinates'] =  {
                "latitude":serializer.data.get('latitude',None),
                "longitude":serializer.data.get('longitude',None)
            }
        data.pop("longitude")
        data.pop("latitude")

        address = serializer.update(instance=address,validated_data=data)

        return Response(SiteAddressSerializer(address).data)



class ListAddress(generics.ListAPIView):
    permission_classes =(IsSuperuser,)
    serializer_class = SiteAddressSerializer
    queryset = SiteAddress.objects.all()
    pagination_class = AdminVendorPagination

# Confirm user account
class ConfirmAccount(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = ConfirmAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Handle cases where confirmation code is not attached to an account
        user = get_object_or_404(CustomUser, email=serializer.data['email'])
        try:
            
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
        except ConfirmationCode.DoesNotExist:
            return Response(
                {"message": "incorrect confirmation code"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetrievePendingDealOfTheDayRequests(generics.ListAPIView):
    queryset = DealOfTheDayRequest.objects.filter(approved=False)
    serializer_class = DealOfTheDayRequestSerializer
    permission_classes=(IsSuperuser,)
    pagination_class = AdminVendorPagination

class RetrieveApprovedDealOfTheDayRequests(generics.ListAPIView):
    queryset = DealOfTheDayRequest.objects.filter(approved=True)
    serializer_class = DealOfTheDayRequestSerializer
    permission_classes=(IsSuperuser,)
    pagination_class = AdminVendorPagination

class ApproveDOTD(generics.ListCreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = DealOfTheDaySerializer
    pagination_class = AdminVendorPagination
    queryset = DealOfTheDay.objects.all().order_by("-end_date")    

    def post(self, request):
        serializer = ApproveDealOfTheDay(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, uid=serializer.data['product'])

        if serializer.data['overwrite'] == False:
            if DealOfTheDay.objects.filter(is_active=True,end_date__gte=datetime.now()).exists():
                return Response({
                    "message":"Deal of the day is still active"
                },status=status.HTTP_400_BAD_REQUEST)
            else:
                active_deals = DealOfTheDay.objects.filter(is_active=True)
                for deal in active_deals:
                    deal.is_active = False
                    deal.save()
                
                end_date = datetime.now() + timedelta(days=1)
                deal = DealOfTheDay.objects.create(
                    product = product,
                    actual_price = product.price,
                    promo_price = product.discounted_price,
                    end_date = end_date
                )

                try:
                    send_deal_request_approval_mail("Deal Of The Day request approved",{"first_name":product.vendor.user.first_name,"email":product.vendor.user.email},{"date_start":deal.start_date,"date_end":deal.end_date})
                except Exception as e:
                    print(e)
                
                return Response(
                    {"message":"Successful"},status=status.HTTP_200_OK
                )
        else:
            active_deals = DealOfTheDay.objects.filter(is_active=True)
            for deal in active_deals:
                deal.is_active = False
                deal.save()
            
            end_date = datetime.now() + timedelta(days=1)
            deal = DealOfTheDay.objects.create(
                product = product,
                actual_price = product.price,
                promo_price = product.discounted_price,
                end_date = end_date
            )

            # deal_request.approved=True
            # deal_request.deal_start= datetime.now()
            # deal_request.deal_end = end_date
            # deal_request.save()
            
            try:
                send_deal_request_approval_mail("Deal Of The Day request approved",{"first_name":product.vendor.user.first_name,"email":product.vendor.user.email},{"date_start":deal.start_date,"date_end":deal.end_date})
            except Exception as e:
                print(e)
            
            return Response(
                {"message":"Successful"},status=status.HTTP_200_OK
            )

class RetrieveRemoveUpdateDOTD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = DealOfTheDaySerializer
    pagination_class = AdminVendorPagination
    queryset = DealOfTheDay.objects.all()
    lookup_field = "uid"

    def partial_update(self, request, uid):
        dotd = get_object_or_404(DealOfTheDay,uid=uid)

        if dotd.is_active:
            dotd.is_active = False
        else:
            deals = DealOfTheDay.objects.filter(is_active=True)

            for deal in deals:
                deal.is_active = False
                deal.save()

            dotd.is_active=True
            dotd.end_date = datetime.now() + timedelta(days=1)

        dotd.save()

        return Response(
            {"message":"Successful"},status=status.HTTP_200_OK
        )



class DeclineDOTDRequest(APIView):
    permission_classes = (IsSuperuser,)
    serializer_class = DeclineDealOfTheDay


    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        deal_request = get_object_or_404(DealOfTheDayRequest,uid=serializer.data['deal_request'])

        deal_request.status = 'declined'
        deal_request.note = "" if serializer.data.get('note',None) == None else serializer.data['note']
        deal_request.save()
        return Response({
            "message":"Successful"
        },status=status.HTTP_200_OK)

class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all().order_by('-created_at')
    serializer_class = VendorSerializer
    permission_classes = (IsSuperuser,)
    lookup_field = 'user__uid'
    pagination_class = AdminVendorPagination

    def destroy(self, request, user__uid):
        user = get_object_or_404(CustomUser, uid=user__uid)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, user__uid):
        serializer = VendorSerializer3(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor = get_object_or_404(Vendor, user__uid=user__uid)

        vendor = serializer.update(vendor,serializer.validated_data)

        return Response(self.serializer_class(vendor).data,status=status.HTTP_200_OK)

    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = (IsSuperuser,)
    lookup_field = 'slug'
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.create(serializer.validated_data)
        product.is_active = True
        product.is_approved =True
        product.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = MainCategorySerializer
    permission_classes = (IsSuperuser,)
    lookup_field = 'slug'
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter

class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all().order_by("name")
    serializer_class = SubCategorySerializer
    permission_classes = (IsSuperuser,)
    lookup_field = 'slug'
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubCategoryFilter

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.create(serializer.validated_data)

        return Response(self.serializer_class(data).data,status=status.HTTP_201_CREATED)

    def partial_update(self,request, slug):
        serializer = CategoryUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sub_cat = get_object_or_404(SubCategory, slug=slug)

        sub_cat = serializer.update(sub_cat,serializer.validated_data)

        return Response(self.serializer_class(sub_cat).data,status=status.HTTP_200_OK)

class ApproveProduct(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request, uid):
        print(uid)
        product = get_object_or_404(Product, uid=uid)

        product.is_active =True
        product.is_approved =True
        product.save()

        return Response({
            "message":"Successful"
        },status=status.HTTP_200_OK)

class DisapproveProduct(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request, uid):
        product = get_object_or_404(Product, uid=uid)

        product.is_active =False
        product.is_approved =False
        product.save()

        return Response({
            "message":"Successful"
        },status=status.HTTP_200_OK)


class SuspendVendor(APIView):
    serializer_class = SuspendVendorSerializer
    permission_classes = (IsSuperuser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = get_object_or_404(Vendor,user__uid=serializer.data['uid'])

        vendor.suspended = not vendor.suspended
        vendor.save()

        return Response({
            "message":"Successful"
        },status=status.HTTP_200_OK)
    

class BankDetailsView(ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = PaymentMethodSerializer2

    def get(self,request,uid):
        payment = PaymentMethods.objects.filter(user__uid=uid)

        page = self.paginate_queryset(payment)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(payment, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class VerifyUnverifyBankDetail(APIView):
    permission_classes=(IsSuperuser,)
    serializer_class = SuspendVendorSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = get_object_or_404(PaymentMethods,uid=serializer.data['uid'])
        payment.verified = not payment.verified
        payment.save()

        return Response({
            "message":"Successful"
        }, status=status.HTTP_200_OK)


class ActiveInactiveBankDetail(APIView):
    permission_classes=(IsSuperuser,)
    serializer_class = SuspendVendorSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = get_object_or_404(PaymentMethods,uid=serializer.data['uid'])
        payment.is_active = not payment.verified
        payment.save()

        return Response({
            "message":"Successful"
        }, status=status.HTTP_200_OK)

class AllOrders(ListAPIView):
    permission_classes= (IsSuperuser,)
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True).order_by('-ordered_date')
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

# class OrderedOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.ORDER_PLACED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class ProcessedOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.PROCESSED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class ShippedOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.SHIPPED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class ConfirmedOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.ORDER_CONFIRMED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class DeliveredOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.DELIVERED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class CancelledOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.CANCELLED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class RefundededOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.REFUNDED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination

# class ReturnedOrders(ListAPIView):
#     permission_classes= (IsSuperuser,)
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('user').prefetch_related('items').filter(ordered=True, status=STATUS.ORDER_RETURNED.value).order_by('-ordered_date')
#     pagination_class = AdminVendorPagination



class UpdateOrderStatus(APIView):
    permission_classes=(IsSuperuser,)
    serializer_class = UpdateOrderStatusSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(Order, uid=serializer.data['order_uid'])
        _status = serializer.data['status']
        date = datetime.now()
        if _status == STATUS.ORDER_CONFIRMED.value:
            order.status = _status
            order.confirmed_date = date
        elif _status == STATUS.PROCESSED.value:
            order.status = _status
            order.processed_date = datetime.now()
        elif _status == STATUS.SHIPPED.value:
            order.status = _status
            order.shipped_date = datetime.now()
        elif _status == STATUS.DELIVERED.value:
            order.status = _status
            order.delivered_date = datetime.now()
        elif _status == STATUS.CANCELLED.value:
            order.status = _status
            order.cancelled_date = datetime.now()
        elif _status == STATUS.ORDER_RETURNED.value:
            order.status = _status
            order.returned_date = datetime.now()
        elif _status == STATUS.REFUNDED.value:
            order.status = _status
            order.refunded_date = datetime.now()
        order.save()
        order.update_order_status(status=_status)

        return Response(
            {"message":"Successful"},status=status.HTTP_200_OK
        )

class DailyOrdersSummary(APIView):
    permission_classes = (IsSuperuser,)
    queryset = Order.objects.all()
    
    def get(self, request):
        queryset = self.queryset.filter(ordered_date__date=datetime.today(), ordered=True)
        result = queryset.aggregate(total=Sum('paid_amount'))
        print(queryset)
        return Response({
            "orders":queryset.count(),
            "today_sale":result['total']
        }, status=status.HTTP_200_OK)

class DailyIncomeSummary(APIView):
    permission_classes = (IsSuperuser,)
    queryset = SaleIncome.objects.filter(income_for="admin", created_at__date=datetime.today(), status="paid")
    
    def get(self, request):
        result = self.queryset.aggregate(total=Sum('amount'))

        return Response({
            "transactions":self.queryset.count(),
            "income": 0 if result['total'] == None else result['total']
        }, status=status.HTTP_200_OK)

class MonthlyOrdersSummary(APIView):
    permission_classes = (IsSuperuser,)
    queryset = Order.objects.all()
    serializer_class = MonthSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset.filter(ordered=True, ordered_date__date__month=serializer.data['month'], ordered_date__date__year=serializer.data['year'])
        result = queryset.aggregate(total=Sum('paid_amount'))

        data = queryset.values_list("ordered_date__date__day").annotate(total=Sum('amount'))
        print(data)
        data = [{item[0]:item[1]} for item in data]

        return Response({
            "orders":queryset.count(),
            "month_total":result['total'],
            "data":data
        }, status=status.HTTP_200_OK)

class MonthlyIncomeSummary(APIView):
    permission_classes = (IsSuperuser,)
    queryset = SaleIncome.objects.filter(income_for="admin", status="paid")
    serializer_class = MonthSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset.filter(created_at__date__month=serializer.data['month'], created_at__date__year=serializer.data['year'])
        result = queryset.aggregate(total=Sum('amount'))

        data = queryset.values_list("created_at__date__day").annotate(total=Sum('amount'))

        data = [{item[0]:item[1]} for item in data]

        return Response({
            "transactions":queryset.count(),
            "month_income":result['total'],
            "data":data
        }, status=status.HTTP_200_OK)

class AnnualOrdersSummary(APIView):
    permission_classes = (IsSuperuser,)
    queryset = Order.objects.all()
    serializer_class = AnnualSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset.filter(ordered_date__date__year=serializer.data['year'], ordered=True)
        result = queryset.aggregate(total=Sum('paid_amount'))

        data = queryset.values_list("ordered_date__date__month").annotate(total=Sum('paid_amount'))
        data = [{calendar.month_name[item[0]][:3]:item[1]} for item in data]

        return Response({
            'orders':queryset.count(),
            "annual_total":result['total'],
            "data":data
        }, status=status.HTTP_200_OK)


class AnnualIncomeSummary(APIView):
    permission_classes = (IsSuperuser,)
    queryset = SaleIncome.objects.filter(income_for="admin", status="paid")
    serializer_class = AnnualSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset.filter(created_at__date__year=serializer.data['year'])
        result = queryset.aggregate(total=Sum('amount'))

        data = queryset.values_list("created_at__date__month").annotate(total=Sum('amount'))
        data = [{calendar.month_name[item[0]][:3]:item[1]} for item in data]

        return Response({
            'transactions':queryset.count(),
            "annual_income":result['total'],
            "data":data
        }, status=status.HTTP_200_OK)

class CountsAnalytics(APIView):
    permission_classes = (IsSuperuser,)
    # queryset = Order.objects.all()
    serializer_class = AnnualSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Sales
        queryset_order = Order.objects.filter(ordered_date__date__year=serializer.data['year'], ordered=True)
        data = queryset_order.values_list("ordered_date__date__month").annotate(total=Count('uid'))
        sales = [{calendar.month_name[item[0]][:3]:item[1]} for item in data]

        # Visitors
        queryset_visitor = Visitor.objects.filter(visited_at__date__year=serializer.data['year'])
        data = queryset_visitor.values_list("visited_at__date__month").annotate(total=Count('uid'))
        visitors = [{calendar.month_name[item[0]][:3]:item[1]} for item in data]


        # products
        queryset_product = Product.objects.filter(created_at__year=serializer.data['year'])
        data = queryset_product.values_list("created_at__month").annotate(total=Count('uid'))
        products = [{calendar.month_name[item[0]][:3]:item[1]} for item in data]



        return Response({
            "sales":sales,
            "visitors":visitors,
            "products":products
        }, status=status.HTTP_200_OK)



class RevenueBasedonArea(APIView):
    permission_classes = (IsSuperuser,)
    queryset = SaleIncome.objects.filter(income_for="admin", status="paid")
    serializer_class = AnnualSerializer
    

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        sales = self.queryset.filter(created_at__date__year=serializer.data['year'])
        total = sales.aggregate(total=Sum('amount'))

        data = [{"country":country,"amount":amount} for country,amount in sales.values_list("country__name").annotate(total=Sum('amount'))]

        return Response({
            'orders':sales.count(),
            "annual_total": 0 if total['total'] == None else total['total'],
            "data":data
        }, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyAdminView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminSerializer2
    queryset = Administrator.objects.all()
    permission_classes=(IsSuperuser,)
    lookup_field = "user__uid"


    def get(self, request,user__uid):
        admin = get_object_or_404(Administrator, user__uid=user__uid)

        serializer = AdminSerializer(admin)

        return Response(serializer.data,status=status.HTTP_200_OK)

class CountryView(ModelViewSet):
    permission_classes=(IsSuperuser,)
    serializer_class=CountrySerializer
    queryset = Country.objects.all().order_by('name')
    pagination_class = AdminVendorPagination
    lookup_field = "uid"

    def create(self, request):
        serializer = CountrySerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        shipping_zones = str(request.data.getlist('shipping_zones', [])[0]).replace('[', '').replace(']','').split(',')

        shipping_zones = ShippingFeeZone.objects.filter(uid__in=[uid.strip() for uid in shipping_zones])

        country = Country.objects.create(
            name = serializer.data['name'],
            code = serializer.data['code'],
            tel = serializer.data['tel']
        )
        
        country.shipping_zones.set(shipping_zones)
        return Response(
            self.serializer_class(country).data,status=status.HTTP_201_CREATED
        )
    
    def partial_update(self, request, uid):
        print(request.data)
        serializer = CountrySerializer3(data=request.data)
        serializer.is_valid(raise_exception=True)
        # shipping_zones = []

        country = get_object_or_404(Country,uid=uid)

        if(str(request.data.getlist('shipping_zones', [])) != "[]"):
            shipping_zones = str(request.data.getlist('shipping_zones', [])[0]).replace('[', '').replace(']','').split(',')
        
        shipping_zones = [uuid.strip() for uuid in shipping_zones]

 
        serializer.validated_data['shipping_zones'] = shipping_zones
        a = serializer.update(country,serializer.validated_data)

        print(a)
        
        # country.shipping_zones.set(shipping_zones)
        return Response(
            self.serializer_class(country).data,status=status.HTTP_201_CREATED
        )



class CreateListShippingZonesView(ModelViewSet):
    permission_classes =(IsSuperuser,)
    serializer_class = ShippingFeeZoneSerializer
    queryset = ShippingFeeZone.objects.all().order_by('name')
    pagination_class = AdminVendorPagination


class CustomerViewSet(ModelViewSet):
    permission_classes =(IsSuperuser,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.select_related("country","user").all().order_by('-created_at')
    pagination_class = AdminVendorPagination
    lookup_field = "user__uid"


    def partial_update(self, request, user__uid):
        print(request.data)
        serializer = CustomerSerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = get_object_or_404(Customer, user__uid=user__uid)

        customer = serializer.update(customer,serializer.validated_data)

        return Response(self.serializer_class(customer).data,status=status.HTTP_200_OK)
    
    def retrieve(self, request,user__uid):
        customer = get_object_or_404(Customer,user__uid=user__uid)
        serializer = CustomerSerializer3(customer)
        return Response(serializer.data)
    
    def list(self, request):
        page = self.paginate_queryset(self.queryset)

        if page is not None:
            customers = CustomerSerializer3(self.queryset, many=True, context={"request":request})
            return self.get_paginated_response(customers.data)
        
        customers = CustomerSerializer3(self.queryset, many=True, context={"request":request})
        return Response(customers.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, user__uid):
        user = get_object_or_404(CustomUser, uid=user__uid)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SuspendUnsuspendCustomer(APIView):
    permission_classes =(IsSuperuser,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def post(self, request, uid):
        customer = get_object_or_404(Customer, user__uid=uid)

        customer.suspended = not customer.suspended
        customer.save()

        return Response({"message":"Successful"}, status=status.HTTP_200_OK)


class ActiveCustomer(APIView):
    permission_classes =(IsSuperuser,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def post(self, request, uid):
        customer = get_object_or_404(Customer, user__uid=uid)

        customer.is_active = not customer.is_active
        customer.save()

        return Response({"message":"Successful"}, status=status.HTTP_200_OK)


class RetrieveCustomerOrder(generics.ListAPIView):
    permission_classes =(IsSuperuser,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("-ordered_date")

    def get(self, request,uid):
        orders = self.queryset.filter(user__user__uid=uid, ordered=True)

        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(orders, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdateFeatured(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request, uid):
        product = get_object_or_404(Product,uid=uid)

        product.featured = not product.featured

        product.save()

        return Response({"message":"Successful"}, status=status.HTTP_200_OK) 


class AddProductToFlashSales(APIView):
    permission_classes=(IsSuperuser,)
    serializer_class = AddFlashSaleSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product,uid=serializer.data['product'])

        flashsale = FlashSale.objects.filter(product=product)

        if flashsale.exists():
            sale = flashsale[0]
            sale.end_date = serializer.data['end_date']
            sale.start_date = datetime.now()
            sale.save()
        else:
            FlashSale.objects.create(
                product = product,
                end_date = serializer.data['end_date']
            )
        return Response({
            "message":"successful"
        }, status=status.HTTP_200_OK)

class RetrieveFlashSaleRequest(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    queryset = FlashSaleRequest.objects.all().order_by('-created_at')
    pagination_class = AdminVendorPagination
    serializer_class = FlashSaleRequestSerializer3


class UpdateDeleteRetrieveFlashSaleRequest(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    queryset = FlashSaleRequest.objects.all().order_by('-created_at')
    pagination_class = AdminVendorPagination
    serializer_class = FlashSaleRequestSerializer
    lookup_field = "uid"

    def get(self, request, uid):
        sale_request = get_object_or_404(FlashSaleRequest, uid=uid)

        serializer = FlashSaleRequestSerializer3(sale_request)

        return Response(serializer.data)

class ApproveFlashSaleRequest(APIView):
    permission_classes = (IsSuperuser,)
    queryset = FlashSaleRequest.objects.all()
    serializer_class = FlashSaleRequestSerializer

    def post(self, request, uid):
        sale_request = get_object_or_404(FlashSaleRequest,uid=uid)

        sale_request.is_approved = True

        sale_request.save()

        flash_sale = FlashSale.objects.create(
         product = sale_request.product,
         end_date = sale_request.end_date,
         start_date = sale_request.start_date,
         stock = sale_request.stock
        )

        send_flashsale_approval_mail("FlashSale request approved",{"first_name":sale_request.product.vendor.user.first_name,"email":sale_request.product.vendor.user.email},{"date_start":flash_sale.start_date,"date_end":flash_sale.end_date})

        return Response(
            {
                "message":"Successful"
            },status=status.HTTP_200_OK
        )


class BannerViewSets(ModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = (IsSuperuser,)
    queryset = Banner.objects.all()
    pagination_class = AdminVendorPagination
    lookup_field = "uid"

class BannerStatus(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request, uid):
        banner = get_object_or_404(Banner, uid=uid)

        banner.is_active = not banner.is_active

        banner.save()

        return Response({
            "message":"Successful"
        }, status=status.HTTP_200_OK)


class PrivacyPolicy(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'privacy_policy.html'
    permission_classes = ()

    def get(self, request):
        return Response(template_name=self.template_name)

class TermsNConditions(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'terms.html'
    permission_classes = ()

    def get(self, request):
        return Response(template_name=self.template_name)


class ListContactMessages(generics.ListAPIView):
    permission_classes=(IsSuperuser,)
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()
    pagination_class = AdminVendorPagination


class TestimonialViewSet(ModelViewSet):
    queryset = Testimonial.objects.all()
    permission_classes = (IsSuperuser,)
    serializer_class = TestimonialSerializer
    pagination_class = AdminVendorPagination


class AllSubscribers(ListAPIView):
    queryset = NewsLetterSubscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = (IsSuperuser,)
    pagination_class = AdminVendorPagination

    def get(self, request):
        query = self.request.query_params.get('status',None)
        subscribers = self.queryset.all()

        if query is not None:
            if query == "verified":
                subscribers = self.queryset.filter(is_verified=True)
            elif query == "unverified":
                subscribers = self.queryset.filter(is_verified=False)

        page = self.paginate_queryset(subscribers)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(subscribers, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
        

class SocialMediaViewSet(ModelViewSet):
    queryset = SocialMedia.objects.all().order_by('handle')
    permission_classes = (IsSuperuser,)
    serializer_class = SocialMediaSerializer
    pagination_class = AdminVendorPagination


class SocialMediaStatus(APIView):
    queryset = SocialMedia.objects.all()
    permission_classes = (IsSuperuser,)

    def post(self, request, uid):
        social = get_object_or_404(SocialMedia, uid=uid)

        social.is_active = not social.is_active

        social.save()

        return Response({
            "message":"Successful"
        }, status=status.HTTP_200_OK)


class SizeModelViewset(ModelViewSet):
    serializer_class = SizeSerializer
    permission_classes = (IsSuperuser,)
    queryset = Size.objects.all()
    pagination_class = AdminVendorPagination

class ColorModelViewset(ModelViewSet):
    serializer_class = ColorSerializer
    permission_classes = (IsSuperuser,)
    queryset = Color.objects.all()
    pagination_class = AdminVendorPagination



class CountVisitor(generics.CreateAPIView):
    model = Visitor
    permission_classes = ()
    serializer_class = VisitorSerializer


@api_view(["GET"])
@permission_classes([IsSuperuser,])
def export_product(request):
    approved = request.query_params.get('approved',None)

    if approved is not None:
        qs = Product.objects.select_related("category").prefetch_related("sub_categories").filter(is_active=True,is_approved=approved)
    else:
        qs = Product.objects.select_related("category")\
        .prefetch_related("sub_categories")\
        .filter(is_active=True)\
        .values("uid","name","sku","category","sub_categories","slug",
        "stock","price", "discount_type","discounted_price","description","additional_info","thumbnail",
        "colors","sizes","tags","featured","vendor","is_approved","is_active","rating","created_at","updated_at"
        )
    return render_to_csv_response(qs)


@api_view(["GET"])
@permission_classes([IsSuperuser,])
def export_vendors(request):
    qs = Vendor.objects.select_related('user').values(
        "user__uid","user__email","user__first_name","user__last_name",
        "user__is_confirmed","shop_name","slug","country__name","address","description","phone_number",
        "pending_balance","balance","featured","closed","user__avatar","banner","created_at","updated_at"
        )
    return render_to_csv_response(qs)

@api_view(["GET"])
@permission_classes([IsSuperuser,])
def export_customers(request):
    qs = Customer.objects.select_related('user').values(
        "user__uid","user__email","user__first_name","user__last_name",
        "user__is_confirmed","user__avatar","country__name","city","address","phone_number",
        "is_active","suspended","created_at","updated_at"
        )
    return render_to_csv_response(qs)



class ProductsCategoriesCount(APIView):
    permission_classes = (IsSuperuser,)

    def get(self, request):
        approved_products = Product.objects.values("uid", "is_approved").filter(is_approved=True).count()
        unapproved_products = Product.objects.values("uid", "is_approved").filter(is_approved=False).count()
        active_approved = Product.objects.values("is_active", "is_approved").filter(is_approved=True, is_active=True).count()
        active_products = Product.objects.values("uid", "is_active").filter(is_active=True).count()
        inactive_products = Product.objects.values("uid", "is_active").filter(is_active=False).count()

        active_cat = Category.objects.values("uid", "is_active").filter(is_active=True).count()
        inactive_cat = Category.objects.values("uid", "is_active").filter(is_active=False).count()

        active_subcat = SubCategory.objects.values("uid", "is_active").filter(is_active=True).count()
        inactive_subcat= SubCategory.objects.values("uid", "is_active").filter(is_active=False).count()

        return Response({
            "product":{
                "approved_products":approved_products,
                "unapproved_products":unapproved_products,
                "active_products":active_products,
                "inactive_products":inactive_products,
                "active_and_approved":active_approved
            },
            "category":{
                "active_categories":active_cat,
                "inactive_categories":inactive_cat,
            },
            "subcategory":{
                "active_subcategories":active_subcat,
                "inactive_subcategories":inactive_subcat,
            },
        })
            


