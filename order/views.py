from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from django.db.models import Sum

from customer.models import Customer
from order.filters import OrderItemFilter
from transactions.models import SaleIncome
from vendor.paginations import AdminVendorPagination, ClientPagination
from vendor.permissions import IsVendor
from vendor.serializers import UpdateOrderStatusSerializer
from .models import Order,OrderItem, ShippingAddress
from product.models import Color, Product, Size
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import AddAddressToCartSerializer, AddQuantitySerializer, AddToCartSerializer, AnnualSerializer, MonthSerializer, OrderItemSerializer, OrderSerializer, OrderSerializer2, RemoveFromCartSerializer, ShippingAddressCreateSerializer, ShippingAddressListSerializer
from customer.permissions import IsCustomer

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.views import APIView

import calendar
from django_filters import rest_framework as filters


@api_view(["POST"])
@permission_classes([IsCustomer])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    uid = serializer.data['uid']
    quantity = serializer.data['quantity']
    price = serializer.data['price']
    user = Customer.objects.get(user=request.user)
    item = get_object_or_404(Product, uid=uid)
    color = get_object_or_404(Color,id=serializer.data['color'])
    size = get_object_or_404(Size,id=serializer.data['size'])

    
    order_item = OrderItem.objects.create(
        item=item,
        user=user,
        ordered=False,
        quantity = quantity,
        price = price,
        size =size,
        color=color
        )

    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # #check if order item is in the order
        # if order.items.filter(item__uid=item.uid).exists():
        #     order_item.quantity += quantity
        #     order_item.save()
        #     return Response({
        #         "message":"Item has been updated"
        #     }, status=status.HTTP_200_OK)
        # else:
        order.items.add(order_item)
        return Response(
            {
                "message": "Item has been added to your cart."
            }, status=status.HTTP_200_OK
        )
    else:
        ordered_date = datetime.now()
        order = Order.objects.create(user=user, ordered_date=ordered_date)
        order.save()
        order.items.add(order_item)
        return Response(
            {
                "message": "Item has been added to your cart."
            }, status=status.HTTP_200_OK
            )


@api_view(["POST"])
@permission_classes([IsCustomer])
def remove_from_cart(request):
    serializer = RemoveFromCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order_item = get_object_or_404(OrderItem,uid=serializer.data['uid'])

    order_item.delete()

    return Response({
        "message":"Item has been removed"
    },status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsCustomer])
def add_item_quantity(request):
    serializer = AddQuantitySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order_item = get_object_or_404(OrderItem,uid=serializer.data['uid'])
    print(serializer.data['quantity'])
    order_item.quantity += serializer.data['quantity']
    order_item.save()


    return Response({
        "message":"Item has been updated"
    },status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsCustomer])
def substract_item_quantity(request):
    serializer = RemoveFromCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order_item = get_object_or_404(OrderItem,uid=serializer.data['uid'])



    if order_item.quantity == 1:
        order_item.delete()

        return Response({
        "message":"Item has been removed"
         },status=status.HTTP_200_OK)


    order_item.quantity -= 1
    order_item.save()

    return Response({
        "message":"Item has been updated"
    },status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsCustomer])
def set_item_quantity(request):
    serializer = AddQuantitySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order_item = get_object_or_404(OrderItem,uid=serializer.data['uid'])

    order_item.quantity = serializer.data['quantity']
    order_item.save()


    return Response({
        "message":"Item has been updated"
    },status=status.HTTP_200_OK)



class VendorOrder(generics.ListAPIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    serializer_class = OrderItemSerializer
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderItemFilter

    def get_queryset(self):
        print("djskjdksj")
        orderitems = OrderItem.objects.select_related('item').filter(ordered=True, item__vendor__user__uid=self.request.user.uid).order_by('-ordered_date')
        print(orderitems)
        return orderitems

# class VendorShippedOrder(generics.ListAPIView):
#     permission_classes = (IsVendor,)
#     authentication_class = JSONWebTokenAuthentication
#     serializer_class = OrderItemSerializer
#     pagination_class = AdminVendorPagination
#     queryset = OrderItem.objects.select_related('item').filter(status="shipped", ordered=True)

#     def get(self, request):
#         orderitems = self.queryset.filter(item__vendor__user__uid=request.user.uid).order_by('-ordered_date')

#         page = self.paginate_queryset(orderitems)
#         if page is not None:
#             serializer = self.serializer_class(page, many=True, context={'request': request})
#             return self.get_paginated_response(serializer.data)

#         serializer = self.serializer_class(orderitems, many=True, context={'request': request})
#         return Response(serializer.data,status=status.HTTP_200_OK)


class VendorArrivedOrder(generics.ListAPIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    serializer_class = OrderItemSerializer
    pagination_class = AdminVendorPagination
    queryset = OrderItem.objects.select_related('item').filter(status="delivered", ordered=True)

    def get(self, request):
        orderitems = self.queryset.filter(item__vendor__user__uid=request.user.uid).order_by('-ordered_date')

        page = self.paginate_queryset(orderitems)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(orderitems, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class UpdateOrderStatus(APIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    serializer_class = UpdateOrderStatusSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(OrderItem, uid=serializer.data['uid'])
        product.status = 'shipped'
        product.shipped_date = datetime.now()
        product.save()
        return Response({
            "message":"Order status has been updated to shipped"
        }, status=status.HTTP_200_OK)


class DailySalesTotal(APIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    # serializer_class = UpdateOrderStatusSerializer
    queryset = OrderItem.objects.select_related('item').filter(ordered=True, ordered_date__date=datetime.today())
    
    def get(self, request):
        queryset = self.queryset.filter(item__vendor__user__uid=request.user.uid)
        result = queryset.aggregate(total=Sum('total_amount'))
        return Response({
            "orders":queryset.count(),
            "today_sale":result['total']
        }, status=status.HTTP_200_OK)

class MonthlySalesTotal(APIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    serializer_class = MonthSerializer
    queryset = OrderItem.objects.select_related('item').filter(ordered=True)
    
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset.filter(item__vendor__user__uid=request.user.uid, ordered_date__date__month=serializer.data['month'], ordered_date__date__year=serializer.data['year'])
        result = queryset.aggregate(total=Sum('total_amount'))

        data = queryset.values_list("ordered_date__date__day").annotate(total=Sum('total_amount'))
        data = [{item[0]:item[1]} for item in data]

        # serializer_data =
        # print(queryset)
        return Response({
            "orders":queryset.count(),
            "month_total":result['total'],
            "data":data
        }, status=status.HTTP_200_OK)

class AnnualSalesTotal(APIView):
    permission_classes = (IsVendor,)
    # authentication_class = JSONWebTokenAuthentication
    serializer_class = AnnualSerializer
    queryset = OrderItem.objects.select_related('item').filter(ordered=True)
    
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset.filter(item__vendor__user__uid=request.user.uid, ordered_date__date__year=serializer.data['year'])
        result = queryset.aggregate(total=Sum('total_amount'))

        data = queryset.values_list("ordered_date__date__month").annotate(total=Sum('total_amount'))
        data = [{calendar.month_name[item[0]]:item[1]} for item in data]

        return Response({
            'orders':queryset.count(),
            "annual_total":result['total'],
            "data":data
        }, status=status.HTTP_200_OK)

class RevenueBasedonArea(APIView):
    permission_classes = (IsVendor,)
    queryset = SaleIncome.objects.filter(income_for="vendor", status="paid")
    serializer_class = AnnualSerializer
    

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        sales = self.queryset.filter(created_at__date__year=serializer.data['year'])
        total = sales.aggregate(total=Sum('amount'))

        data = sales.values_list("country__name").annotate(total=Sum('amount'))

        return Response({
            'orders':sales.count(),
            "annual_total": 0 if total['total'] == None else total['total'],
            "data":data
        }, status=status.HTTP_200_OK)


class RevenueBasedonArea(APIView):
    permission_classes = (IsVendor,)
    queryset = SaleIncome.objects.filter(income_for="vendor", status="paid")
    serializer_class = AnnualSerializer
    

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        sales = self.queryset.filter(created_at__date__year=serializer.data['year'], user=request.user.uid)
        total = sales.aggregate(total=Sum('amount'))

        data = [{"country":country,"amount":amount} for country,amount in sales.values_list("country__name").annotate(total=Sum('amount'))]

        return Response({
            'orders':sales.count(),
            "annual_total": 0 if total['total'] == None else total['total'],
            "data":data
        }, status=status.HTTP_200_OK)



class ClientRetriveOrder(APIView):
    serializer_class = OrderSerializer2
    queryset = Order.objects.filter(ordered=False)
    permission_classes = (IsCustomer,)

    def get(self, request):
        order,created = self.queryset.get_or_create(user=request.user.customer, ordered=False)
        return Response(self.serializer_class(order).data)


class CreateListShippingAddressView(generics.ListCreateAPIView):
    permission_classes = (IsCustomer,)
    serializer_class = ShippingAddressListSerializer
    pagination_class = ClientPagination

    def get_queryset(self):
        addresses = ShippingAddress.objects.filter(user=self.request.user)
        return addresses

    
    def post(self, request):
        serializer = ShippingAddressCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data.get('default',False):
            for add in ShippingAddress.objects.filter(user=request.user):
                add.default = False
                add.save()

        address = serializer.create(serializer.validated_data)

        return Response(self.serializer_class(address).data, status=status.HTTP_201_CREATED)

# class MakeShippingAddressDefault

class RetrieveUpdateDeleteShippingAddressView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCustomer,)
    serializer_class = ShippingAddressCreateSerializer
    pagination_class = ClientPagination
    lookup_field = "uid"
    
    def get_queryset(self):
        addresses = ShippingAddress.objects.filter(user=self.request.user)
        return addresses

    def get(self, request, uid):
        address = get_object_or_404(ShippingAddress, uid=uid)

        serializer = ShippingAddressListSerializer(address)

        return Response(serializer.data)


class AddAddressToCart(APIView):
    permission_classes =(IsCustomer,)
    serializer_class = AddAddressToCartSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = get_object_or_404(ShippingAddress,uid=serializer.data.get('address_uid',None))

        order,created = Order.objects.get_or_create(user=request.user.customer,ordered=False)

        order.shipping_address = address

        order.recipient_name = address.recipient_name
        order.email = address.email
        order.phone = address.phone
        order.country = address.country
        order.address = address.address

        order.save()

        return Response({
            "message":"Shipping address has been updated"
        }, status=status.HTTP_200_OK)

class RemoveAddressToCart(APIView):
    permission_classes =(IsCustomer,)
    serializer_class = AddAddressToCartSerializer

    def patch(self, request):
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # address = get_object_or_404(ShippingAddress,uid=serializer.data.get('address_uid',None))

        order,created = Order.objects.get_or_create(user=request.user.customer,ordered=False)

        order.shipping_address = None

        order.recipient_name = ""
        order.email = ""
        order.phone = ""
        order.country = None
        order.address = ""

        order.save()

        return Response({
            "message":"Shipping address has been removed"
        }, status=status.HTTP_200_OK)










