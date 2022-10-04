from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from vendor.models import CustomUser
from vendor.serializers import CountrySerializer

from .models import Administrator, Country, SiteAddress, SiteConfiguration
from .permissions import IsSuperuser
from .serializers import AdminSerializer, SiteAddressSerializer, SiteConfigSerializer, UserLoginSerializer



class ListandCreateAdmin(generics.ListCreateAPIView):
    permission_classes = (IsSuperuser,)
    queryset = Administrator.objects.all()
    serializer_class = AdminSerializer


class AdminLogin(APIView):
    permission_classes =()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = CustomUser.objects.get(email=serializer.data['email']).uid
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'uid':uid,
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class ListCountries(APIView):
    permission_classes=()
    serializer_class = CountrySerializer

    def get(self, request):
        countries = Country.objects.all()

        serializer = self.serializer_class(countries, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class GetSiteInfo(APIView):
    permission_classes =()
    serializer_class = SiteConfigSerializer

    def get(self,request):
        config = SiteConfiguration.objects.get()
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
    serializer_class = SiteAddressSerializer


    def post(self,request):
        config = SiteConfiguration.objects.get()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.create(serializer.validated_data)

        config.addresses.add(address)
        config.save()

        return Response({
            "message":"Address has been saved"
        },status=status.HTTP_200_OK)

class UpdateAddress(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =(IsSuperuser,)
    serializer_class = SiteAddressSerializer
    queryset = SiteAddress.objects.all()


# class RetrieveDealOfTheDayRequests






