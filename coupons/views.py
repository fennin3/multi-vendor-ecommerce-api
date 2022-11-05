from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from coupons.filters import CouponFilter

from coupons.models import Coupon, UsedCoupon
from coupons.serializers import ApplyCouponSerializer, CouponSerializer
from administrator.permissions import IsSuperuser
from order.models import Order
from vendor.paginations import AdminVendorPagination, ClientPagination

from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from customer.permissions import IsCustomer
from itertools import chain
import datetime
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class CouponAdminModelViewset(ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permission_classes = (IsSuperuser,)
    pagination_class = AdminVendorPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CouponFilter


class ClientCouponListView(ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = (IsCustomer,)
    pagination_class = ClientPagination
    

    def get_queryset(self):
        queryset = Coupon.objects.filter(Q(expire_at__gt=datetime.datetime.now())|Q(expire_at=None), is_active=True)
        customer = self.request.user.customer  
        used_coupons = UsedCoupon.objects.filter(user=self.request.user)

        coupons1 = []

        if customer.is_newbie():
            coupons1 = queryset.filter(condition="newbies")

        coupons2 = queryset.filter(condition="orders", min_orders__lte=200)

        coupons3 = queryset.exclude(condition__in=['newbies',"orders"])


        # merging querysets
        coupons = sorted(chain(coupons1,coupons2, coupons3), key=lambda instance: instance.discount_amount, reverse=True)
        
        results = [coupon for coupon in coupons if not used_coupons.filter(coupon_code=coupon.code).exists() or used_coupons.filter(coupon_code=coupon.code).count() < coupon.no_times]
        
        return results
    
class CartCouponListView(ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = (IsCustomer,)
    pagination_class = ClientPagination
    queryset = Coupon.objects.filter(Q(expire_at__gt=datetime.datetime.now())|Q(expire_at=None), is_active=True)

    def get(self, request, uid):
        order = get_object_or_404(Order, uid=uid)
        customer = request.user.customer  
        used_coupons = UsedCoupon.objects.filter(user=self.request.user)

        coupons1 = []

        if customer.is_newbie():
            coupons1 = self.queryset.filter(condition="newbies")

        coupons2 = self.queryset.filter(condition="orders", min_orders__lte=customer.total_orders())

        coupons3 = self.queryset.filter(condition="amount", min_amount__lte=order.get_total())

        coupons4 = self.queryset.filter(condition="product", product__in=[item.item for item in order.items.all()])

        coupons5 = self.queryset.filter(condition="shipping")

        # merging querysets
        coupons = sorted(chain(coupons1,coupons2, coupons3, coupons4,coupons5), key=lambda instance: instance.discount_amount, reverse=True)
        results = [coupon for coupon in coupons if not used_coupons.filter(coupon_code=coupon.code).exists() or used_coupons.filter(coupon_code=coupon.code).count() < coupon.no_times]

        page = self.paginate_queryset(results)

        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(results, many=True, context={'request': request})
        return Response(serializer.data)

class ApplyCoupon(APIView):
    permission_classes = (IsCustomer,)
    serializer_class = ApplyCouponSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(Order,uid=serializer.data['order_uid'])
        coupon = get_object_or_404(Coupon, code=serializer.data['code'])

        success,message = coupon.can_use(user=request.user,order=order)
        
        if success:     
            order.coupon_used = coupon
            order.save()

            return Response(
                {
                    "message":"Successful"
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message":message
                }, status=status.HTTP_400_BAD_REQUEST
            )


