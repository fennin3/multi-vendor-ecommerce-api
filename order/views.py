from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from django.db.models import Sum

from customer.models import Customer
from vendor.paginations import AdminVendorPagination
from vendor.permissions import IsVendor
from vendor.serializers import UpdateOrderStatusSerializer
from .models import Order,OrderItem
from product.models import Color, Product, Size
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import AddToCartSerializer, AnnualSerializer, MonthSerializer, OrderItemSerializer
from customer.permissions import IsCustomer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.views import APIView

import calendar

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


class VendorAllOrder(generics.ListAPIView):
    permission_classes = (IsVendor,)
    authentication_class = JSONWebTokenAuthentication
    pagination_class = AdminVendorPagination
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.select_related('item').filter(ordered=True)

    def get(self, request):
        orderitems = self.queryset.filter(item__vendor__user__uid=request.user.uid).order_by('-ordered_date')

        page = self.paginate_queryset(orderitems)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(orderitems, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class VendorOrder(generics.ListAPIView):
    permission_classes = (IsVendor,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = OrderItemSerializer
    pagination_class = AdminVendorPagination
    queryset = OrderItem.objects.select_related('item').filter(ordered=True)

    def get(self, request, status):
        orderitems = self.queryset.filter(status=status,item__vendor__user__uid=request.user.uid).order_by('-ordered_date')

        page = self.paginate_queryset(orderitems)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(orderitems, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

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
    authentication_class = JSONWebTokenAuthentication
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
    authentication_class = JSONWebTokenAuthentication
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
    authentication_class = JSONWebTokenAuthentication
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
    authentication_class = JSONWebTokenAuthentication
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
    authentication_class = JSONWebTokenAuthentication
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
