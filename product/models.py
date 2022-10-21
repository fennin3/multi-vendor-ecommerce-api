from email.policy import default
from enum import unique
import uuid
from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model

# Form Images
from io import BytesIO
from PIL import Image as IMG
from django.core.files import File

from django.db import models


User = get_user_model()

class Color(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=5)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to="media/Category-Avatar/")
    slug =AutoSlugField(populate_from="name",unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'   

    def __str__(self):
        return self.name
     


class SubCategory(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug =AutoSlugField(populate_from="name",unique=True)
    avatar = models.ImageField(upload_to="media/SubCategory-Avatar/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'


    def __str__(self):
        return self.name

from vendor.models import Vendor


class Tag(models.Model):
    name=models.CharField(max_length=10)

class Product(models.Model):
    DISCOUNT_TYPE = (
        ("PCT","PCT"),
        ("AMT","AMT")
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    sub_categories = models.ManyToManyField(SubCategory, related_name='sub_products')
    slug = AutoSlugField(populate_from="name")
    stock = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_type = models.CharField(max_length=25, choices=DISCOUNT_TYPE, default="AMT")
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discounted_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=False, default="")
    additional_info = models.JSONField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="media/Products-Avatar/", blank=True, null=True)
    thumbnail_created = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color,default=[])
    sizes = models.ManyToManyField(Size, default=[])
    tags = models.ManyToManyField(Tag, blank=True, related_name="tag_products")
    featured = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor')
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.thumbnail_created:
            self.thumbnail = self.make_thumbnail(self.thumbnail)
            self.thumbnail_created = True

        if self.discount > 0.00:
            if self.discount_type == "AMT":
                self.discounted_price = self.price - self.discount
            else:
                self.discounted_price  = self.price - (self.price * self.discount)
        super(Product, self).save(*args, **kwargs)

    def make_thumbnail(self, image, size=(350, 350)):
        img = IMG.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'webp', optimize=True, quality=95)
        filename= str(image.name).split('.')[0]
        thumbnail = File(thumb_io, name=filename + '.webp')

        return thumbnail


class Image(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(unique=True, upload_to="media/Products-Avatar/")

    def __str__(self):
        return f"{self.image.url}"

class Review(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rate = models.FloatField()
    review = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductVariation(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    size = models.ForeignKey(Size, null=True,blank=True, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DealOfTheDay(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    actual_price = models.DecimalField(max_digits=15, decimal_places=2)
    promo_price = models.DecimalField(max_digits=15, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()


    class Meta:
        # ordering = ('name',)
        verbose_name = 'Deal the day'
        verbose_name_plural = 'Deal of the day' 


class FlashSaleRequest(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="flash_sales")
    days = models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class FlashSale(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=False, null=False)

