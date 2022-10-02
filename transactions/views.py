from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from .models import PaymentMethods
from .serializers import PaymentMethodSerializer
from vendor.permissions import IsVendor

class AddPaymentMethod(CreateAPIView):
    permission_classes = (IsVendor,)
    serializer_class = PaymentMethodSerializer



class RetrievePaymentMethod(RetrieveDestroyAPIView):
    permission_classes = (IsVendor,)
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethods.objects.all()
    lookup_field = 'uid'

class UpdatePaymentMethod(UpdateAPIView):
    permission_classes = (IsVendor,)
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethods.objects.all()
    lookup_field = 'uid'
