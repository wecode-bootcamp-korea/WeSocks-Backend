from django.db import models
from django.utils import timezone
from user.models import User, UserType
from product.models import *

class WishesDetail(models.Model):
    # wisher
    user        = models.ForeignKey(User, on_delete = models.SET_NULL, null =True)
    label       = models.CharField(max_length = 50, blank = True, null = True)
    design      = models.ForeignKey(DesignDescription, on_delete = models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "wish_list"

class CartDetail(models.Model):
    # cart adder
    user           = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    label          = models.CharField(max_length = 50, blank = True, null = True)
    design         = models.ForeignKey(DesignDescription, on_delete = models.CASCADE)
    count          = models.IntegerField()
    total_price    = models.DecimalField(blank = True, null = True, max_digits = 10, decimal_places = 2)
    reward_points  = models.DecimalField(blank = True, null = True, max_digits = 10, decimal_places = 2, default = 0)
    created_at     = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "cart_list"
