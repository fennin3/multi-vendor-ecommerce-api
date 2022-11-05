import uuid
import django
from django.db import models
from administrator.utils import STATUS
from coupons.models import Coupon
from order.utils import generate_order_id
from product.models import Color, Product, Size
from customer.models import Customer
import datetime
from decimal import Decimal, getcontext
from administrator.models import Country
from django.contrib.auth import get_user_model

getcontext().prec = 2
User = get_user_model()

class ShippingAddress(models.Model):
    uid = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipping_addressed")
    recipient_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=100,blank=True, null=True)
    phone = models.CharField(max_length=16)    
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.recipient_name
    

class OrderItem(models.Model):
    STATUS_CHOICES = (
        ('pending','pending'),
        ('order_placed', 'order_placed'),
        ('order_confirmed', 'order_confirmed'),
        ('processed', 'processed'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),
        ('order_returned', 'order_returned'),
        ('refunded', 'refunded'),
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_items")
    size = models.ForeignKey(Size,related_name="size_products", on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color,related_name="size_products", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    discount_price = models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quantity = models.IntegerField(default=1)

    ordered_date = models.DateTimeField(blank=True,null=True)
    confirmed_date = models.DateTimeField(blank=True,null=True)
    processed_date = models.DateTimeField(blank=True,null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    refunded_date = models.DateTimeField(blank=True, null=True)
    returned_date = models.DateTimeField(blank=True, null=True)

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
    STATUS_CHOICES = (
        ('pending','pending'),
        ('order_placed', 'order_placed'),
        ('order_confirmed', 'order_confirmed'),
        ('processed', 'processed'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),
        ('order_returned', 'order_returned'),
        ('refunded', 'refunded'),
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    order_id = models.CharField(max_length=15, default=generate_order_id, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    items = models.ManyToManyField(OrderItem, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    coupon_used = models.ForeignKey(Coupon,null=True, blank=True, on_delete=models.CASCADE)
    transaction_ref = models.CharField(max_length=255,blank=True, null=True)

    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.SET_NULL)

    # Shipping Details
    recipient_name = models.CharField(max_length=1000,null=True,blank=True)
    email = models.EmailField(max_length=100,blank=True, null=True)
    phone = models.CharField(max_length=16, null=True,blank=True)    
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True,blank=True)
    address = models.TextField(blank=True, null=True)

    # Paymment Method
    payment_method = models.JSONField(null=True, blank=True)
    
    # Dates
    ordered_date = models.DateTimeField(blank=True,null=True)
    confirmed_date = models.DateTimeField(blank=True,null=True)
    processed_date = models.DateTimeField(blank=True,null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    refunded_date = models.DateTimeField(blank=True, null=True)
    returned_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order  {self.uid}"



    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_amount

        if self.coupon_used.discount_type == "PCT":
            total -= (total * (self.coupon_used.discount_amount/100))
        else:
            total -= self.coupon_used.discount_amount
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
            item.status
            item.ordered_date = datetime.datetime.now()
            item.save()

    def update_order_status(self, status):
        for item in self.items.all():
            item.status = status
            if status == STATUS.CANCELLED.value:
                item.cancelled_date=self.cancelled_date
            elif status == STATUS.DELIVERED.value:
                item.delivered_date=self.delivered_date
            elif status == STATUS.ORDER_CONFIRMED.value:
                item.confirmed_date=self.confirmed_date
            elif status == STATUS.ORDER_PLACED.value:
                item.ordered_date = self.ordered_date
            elif status == STATUS.ORDER_RETURNED.value:
                item.returned_date = self.returned_date
            elif status == STATUS.PROCESSED.value:
                item.processed_date = self.processed_date
            elif status == STATUS.REFUNDED.value:
                item.refunded_date = self.refunded_date
            elif status == STATUS.SHIPPED.value:
                item.shipped_date = self.shipped_date
            item.save()