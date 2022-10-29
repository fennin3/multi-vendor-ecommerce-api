from rest_framework.viewsets import ModelViewSet

from administrator.permissions import IsSuperuser
from blog.filters import ArticleCategoryFilter, ArticleCommentFilter, ArticleCommentReplyFilter, ArticleFilter
from blog.models import Article, Category, Comment, CommentReply
from blog.serializers import ArticleCategorySerializer, ArticleSerializer, ArticleSerializer2, CommentReplySerializer, CommentReplySerializer2, CommentSerializer, CommentSerializer2
from vendor.paginations import AdminVendorPagination
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

class ClientArticleModelViewset(ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ArticleSerializer2
    pagination_class = AdminVendorPagination
    queryset = Article.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleFilter
    lookup_field = "slug"

class ClientArticleModelViewset2(RetrieveAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ArticleSerializer2
    pagination_class = AdminVendorPagination
    queryset = Article.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleFilter
    lookup_field = "slug"



class ClientArticleCategoryModelViewset(ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ArticleCategorySerializer
    pagination_class = AdminVendorPagination
    queryset = Category.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCategoryFilter
    lookup_field = "slug"


class ClientCommentModelViewset(ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CommentSerializer
    pagination_class = AdminVendorPagination
    queryset = Comment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCommentFilter
    # lookup_field = "slug"



class ClientCommentReplyModelViewset(ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CommentReplySerializer
    pagination_class = AdminVendorPagination
    queryset = CommentReply.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleCommentReplyFilter
    # lookup_field = "slug"


