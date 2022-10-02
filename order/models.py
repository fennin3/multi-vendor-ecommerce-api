from email.policy import default
import uuid
from django.db import models
from product.models import Color, Product, Size
from customer.models import Customer
import datetime
from decimal import Decimal, getcontext


getcontext().prec = 2

ORDERED = 'ordered'
SHIPPED = 'shipped'
ARRIVED = 'arrived'


class OrderItem(models.Model):
    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (ARRIVED, 'Arrived')
        )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size,related_name="size_products", on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color,related_name="size_products", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    discount_price = models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(blank=True,null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    arrived_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.discount_price > 0:
            self.total_amount = Decimal(self.discount_price) * Decimal(self.quantity)
        else:
            self.total_amount = Decimal(self.price) * Decimal(self.quantity)
        super(OrderItem, self).save(*args, **kwargs)

    def get_total_item_price(self):
        return self.price * self.quantity 

    def get_total_discount_item_price(self):
        return self.quantity * self.discount_price


class  Order(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    used_coupon = models.CharField(max_length=50, blank=True, null=True)
    transaction_ref = models.CharField(max_length=255,blank=True, null=True)

    recipient_name = models.CharField(max_length=100,blank=True, null=True)
    email = models.CharField(max_length=100,blank=True, null=True)
    address = models.CharField(max_length=100,blank=True, null=True)
    phone = models.CharField(max_length=100,blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.uid}"



    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


        

    def get_amount_saved(self):
        return self.get_total() - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total() 

    def mark_ordered(self):
        for item in self.items.all():
            item.ordered =True
            item.ordered_date = datetime.datetime.now()
            item.save()