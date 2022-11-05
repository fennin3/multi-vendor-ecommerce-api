from django.db import models
import uuid
from coupons.utils import generate_coupon_code
from product.models import Product
from django.contrib.auth import get_user_model
from itertools import chain
import datetime
from django.db.models import Q 

User = get_user_model()

class UsedCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons_used')
    coupon_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coupon_code}  used by {self.user}"    


class Coupon(models.Model):
    DISCOUNT_TYPE = (
        ("PCT","PCT"),
        ("AMT","AMT")
    )
    CONDITIONS = (
        ('newbies','newbies'),
        ("orders","orders"),
        ("amount","amount"),
        ("product","product"),
        ("shipping","shipping")
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=1000,null=True, blank=True)
    code = models.CharField(max_length=6, blank=True, null=True, unique=True)
    condition = models.CharField(max_length=20, choices=CONDITIONS)
    discount_type = models.CharField(max_length=3, choices=DISCOUNT_TYPE, default="PCT")
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2)
    min_amount= models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    min_orders = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    # sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True,blank=True)
    total_coupons = models.IntegerField()
    available_coupons = models.IntegerField(default=-1)
    no_times = models.IntegerField()
    is_active = models.BooleanField()
    start_at = models.DateTimeField(null=True,blank=True)
    expire_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.code == None or self.code =="":
            while True:
                code = generate_coupon_code()
                if Coupon.objects.filter(code=code).exists():
                    continue
                else:
                    self.code = code
                    break
        if self.available_coupons == -1:
            self.available_coupons = self.total_coupons
        super(Coupon, self).save(*args, **kwargs)


    def __str__(self):
        return self.code
    
    
    def count_coupon_use(self):
        self.available_coupons -= 1
        self.save()
    
    def used_coupons(self):
        used_coupons = UsedCoupon.objects.filter(coupon_code=self.code)
        return used_coupons

    def can_use(self, user, order):
        queryset = Coupon.objects.filter(Q(expire_at__gt=datetime.datetime.now())|Q(expire_at=None), is_active=True)
        if UsedCoupon.objects.filter(user=user).count() == self.no_times:
            return False,"Sorry, you have exceeded the number of times you can use this coupon"
        else:
            customer = user.customer  
            used_coupons = UsedCoupon.objects.filter(user=user)

            coupons1 = []

            if customer.is_newbie():
                coupons1 = queryset.filter(condition="newbies")

            coupons2 = queryset.filter(condition="orders", min_orders__lte=customer.total_orders())

            coupons3 = queryset.filter(condition="amount", min_amount__lte=order.get_total())

            coupons4 = queryset.filter(condition="product", product__in=[item.item for item in order.items.all()])

            coupons5 = queryset.filter(condition="shipping")

            # merging querysets
            coupons = sorted(chain(coupons1,coupons2, coupons3, coupons4,coupons5), key=lambda instance: instance.discount_amount, reverse=True)
            results = [coupon for coupon in coupons if not used_coupons.filter(coupon_code=coupon.code).exists() or used_coupons.filter(coupon_code=coupon.code).count() < coupon.no_times]
            if self in results:
                return True,""
            else:
                return False,"You can not use this coupon"
