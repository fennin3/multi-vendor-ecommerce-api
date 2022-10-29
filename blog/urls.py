from django.urls import path, include
from rest_framework import routers

from blog.views import ClientArticleCategoryModelViewset, ClientArticleModelViewset, ClientCommentModelViewset, ClientCommentReplyModelViewset


router = routers.DefaultRouter(trailing_slash=True)

router.register(r'articles', ClientArticleModelViewset)
router.register(r'categories', ClientArticleCategoryModelViewset)
router.register(r'comments', ClientCommentModelViewset)
router.register(r'replies', ClientCommentReplyModelViewset)

urlpatterns = [
    path('', include(router.urls)),
]
