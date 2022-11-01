from django.db import models
import uuid
from coupons.utils import generate_coupon_code
from product.models import Category, Product, SubCategory
from django.contrib.auth import get_user_model


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
