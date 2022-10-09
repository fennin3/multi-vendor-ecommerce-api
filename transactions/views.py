# from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from vendor.paginations import AdminVendorPagination
from .models import PaymentMethods
from .serializers import PaymentMethodSerializer, PaymentMethodSerializer2
from vendor.permissions import IsVendor
from rest_framework import status



# class AddPaymentMethod(CreateAPIView):
#     permission_classes = (IsVendor,)
#     serializer_class = PaymentMethodSerializer



class ListPaymentMethod(ListCreateAPIView):
    permission_classes = (IsVendor,)
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethods.objects.all()
    pagination_class = AdminVendorPagination


    def get(self,request):
        payments = PaymentMethods.objects.filter(user=request.user)
        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = PaymentMethodSerializer2(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = PaymentMethodSerializer2(payments, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class UpdatePaymentMethod(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsVendor,)
    serializer_class = PaymentMethodSerializer2
    queryset = PaymentMethods.objects.all()
    lookup_field = 'uid'
