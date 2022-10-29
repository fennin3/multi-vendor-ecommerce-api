from rest_framework import serializers

from vendor.serializers import UserSerializer
from .models import Category,Article,Comment,CommentReply





class CommentReplySerializer2(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model=CommentReply
        fields="__all__"

class CommentReplySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model=CommentReply
        fields="__all__"


class CommentSerializer(serializers.ModelSerializer):
    replies = CommentReplySerializer(read_only=True, many=True)
    is_active = serializers.BooleanField(default=True)
    user = UserSerializer(read_only=True) 
    class Meta:
        model=Comment
        fields="__all__"

class CommentSerializer2(serializers.ModelSerializer):
    replies = CommentReplySerializer2(read_only=True, many=True)
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model=Comment
        fields="__all__"


class ArticleSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model=Article
        fields="__all__"

class ArticleCategorySerializer2(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    # articles =
    class Meta:
        model=Category
        fields="__all__"

class ArticleSerializer2(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    comments = CommentSerializer(read_only=True, many=True)
    category = ArticleCategorySerializer2(read_only=True)
    class Meta:
        model=Article
        fields="__all__"


class ArticleCategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    articles =ArticleSerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields="__all__"


