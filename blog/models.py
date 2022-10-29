from autoslug import AutoSlugField
from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()



class Category(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=1000)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="media/Blog-Category/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Article(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=1000)
    slug = AutoSlugField(populate_from="title", unique=True,  null=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to="media/Blog-Article/", null=True, blank=True)
    reads = models.IntegerField(default=0)
    authors = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles")
    is_active = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    rate = models.DecimalField(max_digits=9, decimal_places=1, default=0.0)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uid

    
class CommentReply(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    rate = models.DecimalField(max_digits=9, decimal_places=1, default=0.0)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uid

    


    

    