from rest_framework.viewsets import ModelViewSet

from administrator.permissions import IsSuperuser
from blog.filters import ArticleCategoryFilter, ArticleCommentFilter, ArticleCommentReplyFilter, ArticleFilter
from blog.models import Article, Category, Comment, CommentReply
from blog.serializers import ArticleCategorySerializer, ArticleSerializer, ArticleSerializer2, CommentReplySerializer, CommentReplySerializer2, CommentSerializer, CommentSerializer2
from vendor.paginations import AdminVendorPagination, ClientPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

class ArticleModelViewset(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = ArticleSerializer2
    pagination_class = AdminVendorPagination
    queryset = Article.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleFilter
    lookup_field = "slug"



    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.create(serializer.validated_data)
        
        return Response(self.serializer_class(article).data,status=status.HTTP_201_CREATED)

class ArticleCategoryModelViewset(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = ArticleCategorySerializer
    pagination_class = AdminVendorPagination
    queryset = Category.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCategoryFilter
    lookup_field = "slug"
    



class CommentModelViewset(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = CommentSerializer
    pagination_class = AdminVendorPagination
    queryset = Comment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCommentFilter
    # lookup_field = "slug"

    def create(self, request):
        serializer = CommentSerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.create(serializer.validated_data)
        
        return Response(self.serializer_class(article).data,status=status.HTTP_201_CREATED)


class CommentReplyModelViewset(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = CommentReplySerializer
    pagination_class = AdminVendorPagination
    queryset = CommentReply.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCommentReplyFilter
    # lookup_field = "slug"

    def create(self, request):
        serializer = CommentReplySerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.create(serializer.validated_data)
        
        return Response(self.serializer_class(article).data,status=status.HTTP_201_CREATED)


# ##################

class ClientArticleModelViewset(ModelViewSet):
    permission_classes = ()
    serializer_class = ArticleSerializer2
    pagination_class = ClientPagination
    queryset = Article.objects.filter(is_active=True)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleFilter
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)


class ClientArticleCategoryModelViewset(ModelViewSet):
    permission_classes = ()
    serializer_class = ArticleCategorySerializer
    pagination_class = ClientPagination
    queryset = Category.objects.filter(is_active=True)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCategoryFilter
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)


class ClientCommentModelViewset(ModelViewSet):
    permission_classes = ()
    serializer_class = CommentSerializer
    pagination_class = ClientPagination
    queryset = Comment.objects.filter(is_active=True)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCommentFilter
    # lookup_field = "slug"

    def create(self, request):
        serializer = CommentSerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.create(serializer.validated_data)
        return Response(self.serializer_class(article).data,status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)



class ClientCommentReplyModelViewset(ModelViewSet):
    permission_classes = ()
    serializer_class = CommentReplySerializer
    pagination_class = ClientPagination
    queryset = CommentReply.objects.filter(is_active=True)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCommentReplyFilter
    # lookup_field = "slug"

    def create(self, request):
        serializer = CommentReplySerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.create(serializer.validated_data)
        
        return Response(self.serializer_class(article).data,status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response({
            "message":"You do not have the permission for this"
        },status=status.HTTP_401_UNAUTHORIZED)


