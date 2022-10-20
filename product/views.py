from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import AllowAny

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from vendor.models import Vendor
from vendor.paginations import AdminVendorPagination, CategoryPagination
from vendor.permissions import IsVendor

from .models import Category, Image, Product, SubCategory, Image, ProductVariation, Review, Size
from .serializers import (ImageSerializer, MainCategorySerializer, ProductSerializer, CategorySerializer, ProductSerializer2,
 ReviewSerializer2, SubCategorySerializer, VariantSerializer)



class CategoryView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = SubCategory.objects.all().order_by('name')
    serializer_class = CategorySerializer
    
class ListAllProducts(generics.ListAPIView):
    permission_classes = ()
    queryset = Product.objects.filter(is_active=True,is_approved=True, vendor__suspended=False, vendor__closed=False, category__is_active=True, sub_categories__is_active=True).order_by("-created_at")
    serializer_class = ProductSerializer


class CreateListProduct(generics.ListCreateAPIView):
    permission_classes = (IsVendor,)
    queryset = Product.objects.all().order_by('-created_at')
    pagination_class = AdminVendorPagination
    serializer_class = ProductSerializer2

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        categories =[]
        sizes =[]
        colors =[]

        if serializer.data['sub_categories']:
            categories = str(serializer.data['sub_categories'][0]).replace('[','').replace(']','').split(',')
        if serializer.data['sizes']:
            sizes = str(serializer.data['sizes'][0]).replace('[','').replace(']','').split(',')
        if serializer.data['colors']:
            colors = str(serializer.data['colors'][0]).replace('[','').replace(']','').split(',')
        # colors = request.data.get

        vendor = get_object_or_404(Vendor, user=request.user)

        product = Product.objects.create(
            vendor=vendor,
            name=serializer.data['name'],
            price=serializer.data['price'],
            stock=serializer.data['stock'],
            discount_type=serializer.data['discount_type'],
            discount=serializer.data['discount'],
            thumbnail=request.data['thumbnail'],
            description=serializer.data['description']
        )

        categories = SubCategory.objects.filter(uid__in=[category.strip() for category in categories])
        sizes = Size.objects.filter(id__in=sizes)
        colors = Size.objects.filter(id__in=colors)

        product.sub_categories.set(categories)
        product.sizes.set([size.id for size in sizes])
        product.colors.set([color.id for color in colors])
        
        images_objs = []
        for image in request.data.getlist('images'):
            images_objs.append(Image(product=product, image=image))

        images = Image.objects.bulk_create(images_objs)
        product.save()
        
        return Response(
            {"message": "Product successfully created!"}, status=status.HTTP_201_CREATED
        )


    def get(self, request, vendor_id=None):

        if vendor_id:
            products = self.queryset.filter(vendor__user__uid=vendor_id)
        else:
            products = self.queryset.all()

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class ListVendorProduct(generics.ListAPIView):
    permission_classes = (IsVendor,)
    queryset = Product.objects.all().order_by('-created_at')
    pagination_class = AdminVendorPagination
    serializer_class = ProductSerializer2


    def get(self, request, vendor_id=None):
        status = self.request.query_params.get('approved')

        if vendor_id:
            if status == "true":
                products = self.queryset.filter(vendor__user__uid=vendor_id, is_approved=True)
            elif status == "false":
                products = self.queryset.filter(vendor__user__uid=vendor_id, is_approved=False)
            else:
                products = self.queryset.filter(vendor__user__uid=vendor_id)
        else:
            products = self.queryset.all()

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdateRetrieveDetroyProduct(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsVendor,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "uid"

class UpdateProductStatus(APIView):
    permission_classes = (IsVendor,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def patch(self,request, uid):
        product = self.queryset.get(uid=uid)
        value = product.is_active
        product.is_active = not value
        product.save()
        value = "Active" if product.is_active else "Inactive"
        return Response(
            {
                "message":f"Product is now {value}"
            },status=status.HTTP_200_OK
        )

class DeleteProductImage(generics.DestroyAPIView):
    permission_classes = (IsVendor,)
    queryset =  Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'uid'

class ImageUploadView(generics.CreateAPIView):
    permission_classes = (IsVendor,)
    queryset =  Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, uid):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, uid=uid)
    
        if request.user == product.vendor.user:
            serializer.save(product=product)
            return Response(
                {"message": f"{product.name}'s image successfully added!"}, status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"message": "You don't have necessary permission(s) for this action"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class AddProductVariant(generics.CreateAPIView):
    permission_classes =(IsVendor,)
    queryset = ProductVariation.objects.all()
    serializer_class = VariantSerializer

class UpdateRetrieveDestroyProductVariant(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =(IsVendor,)
    queryset = ProductVariation.objects.all()
    serializer_class = VariantSerializer
    lookup_field = "uid"

class VariantStatus(APIView):
    permission_classes =(IsVendor,)
    queryset = ProductVariation.objects.all()
    serializer_class = VariantSerializer

    def patch(self, request,uid):
        item = self.queryset.get(uid=uid)
        value = item.is_active
        item.is_active = not value
        item.save()
        val = "Active" if item.is_active else "Inactive"
        return Response({
            "message":f"Item is now {val}"
        },status=status.HTTP_200_OK)

class ProductReviewsVendor(generics.ListAPIView):
    permission_classes = (IsVendor,)
    serializer_class = ReviewSerializer2
    pagination_class = AdminVendorPagination
    queryset = Review.objects.select_related('user','product').filter(is_active=True)

    def get(self, request):
        reviews = self.queryset.filter(product__vendor__user=request.user)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(reviews, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class AllCatgories(generics.ListAPIView):
    serializer_class = MainCategorySerializer
    permission_classes =()
    pagination_class = CategoryPagination
    queryset = Category.objects.filter(is_active=True).order_by('name')

class AllSubCatgories(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    permission_classes =()
    pagination_class = CategoryPagination
    queryset = SubCategory.objects.filter(is_active=True).order_by("name")


class CategorySubCategory(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes =()
    pagination_class = CategoryPagination
    queryset = SubCategory.objects.all()

    def get(self, request, uid):
        category = get_object_or_404(Category,uid=uid)

        sub_cats = self.queryset.filter(category=category).order_by("name")

        page = self.paginate_queryset(sub_cats)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(sub_cats, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class CategoryProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes =()
    # pagination_class
    queryset = Product.objects.all().order_by("created_at")

    def get(self, request, uid):
        category = get_object_or_404(Category,uid=uid)

        products = self.queryset.filter(category=category).order_by("created_at")

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(products, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class SubCategoryProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes =()
    # pagination_class
    queryset = Product.objects.all().order_by("created_at")

    def get(self, request, uid):
        subcategory = get_object_or_404(SubCategory,uid=uid)

        products = self.queryset.filter(sub_categories__in=[subcategory]).order_by("created_at")

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(products, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)


# class Mark

