from django.db import models
import uuid

class Category(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="media/Blog-Category/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=1000)
    body = models.TextField()
    image = models.ImageField(upload_to="media/Blog-Article/", null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    

    