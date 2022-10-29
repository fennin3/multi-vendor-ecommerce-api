from django.urls import path, include
from rest_framework import routers

from blog.views import ArticleCategoryModelViewset, ArticleModelViewset, CommentModelViewset, CommentReplyModelViewset


router = routers.DefaultRouter(trailing_slash=True)

router.register(r'articles', ArticleModelViewset)
router.register(r'categories', ArticleCategoryModelViewset)
router.register(r'comments', CommentModelViewset)
router.register(r'replies', CommentReplyModelViewset)

urlpatterns = [
    path('', include(router.urls)),
]
