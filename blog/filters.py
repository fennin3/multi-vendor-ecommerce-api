from django_filters import rest_framework as filters
from .models import Article, Category, Comment, CommentReply

class ArticleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title",lookup_expr='icontains') 
    is_active = filters.BooleanFilter() 
    published = filters.DateFromToRangeFilter(field_name="published_at")

    sort_by = filters.OrderingFilter(fields=(
            ('title', 'title'),
            ('published_at', 'published_at'),
        ))

    class Meta:
        model = Article
        fields = ("category","is_active")



class ArticleCategoryFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title",lookup_expr='icontains') 
    is_active = filters.BooleanFilter() 

    sort_by = filters.OrderingFilter(fields=(
            ('title', 'title'),
            ('created_at', 'created_at'),
        ))

    class Meta:
        model = Category
        fields = ("is_active",)


    
class ArticleCommentFilter(filters.FilterSet):
    body = filters.CharFilter(field_name="body",lookup_expr='icontains') 
    is_active = filters.BooleanFilter() 
    rate_min = filters.NumberFilter(field_name="rate", lookup_expr="gte")
    rate_max = filters.NumberFilter(field_name="rate", lookup_expr="lte")

    sort_by = filters.OrderingFilter(fields=(
            ('created_at', 'created_at'),
        ))

    class Meta:
        model = Comment
        fields = ("is_active",)

class ArticleCommentReplyFilter(filters.FilterSet):
    body = filters.CharFilter(field_name="body",lookup_expr='icontains') 
    is_active = filters.BooleanFilter() 
    rate_min = filters.NumberFilter(field_name="rate", lookup_expr="gte")
    rate_max = filters.NumberFilter(field_name="rate", lookup_expr="lte")

    sort_by = filters.OrderingFilter(fields=(
            ('created_at', 'created_at'),
        ))

    class Meta:
        model = CommentReply
        fields = ("is_active","rate",)


