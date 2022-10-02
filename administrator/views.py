from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from vendor.models import CustomUser
from vendor.serializers import CountrySerializer

from .models import Administrator, Country
from .permissions import IsSuperuser
from .serializers import AdminSerializer


class ListandCreateAdmin(generics.ListCreateAPIView):
    permission_classes = (IsSuperuser,)
    queryset = Administrator.objects.all()
    serializer_class = AdminSerializer

class ListCountries(APIView):
    permission_classes=()
    serializer_class = CountrySerializer

    def get(self, request):
        countries = Country.objects.all()

        serializer = self.serializer_class(countries, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)