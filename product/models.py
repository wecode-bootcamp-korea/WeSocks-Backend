from django.db import models
from django.utils import timezone
from user.models import User, UserType

class SocksCategory(models.Model):
    title = models.CharField(max_length = 50)
    # 1: athletic
    # 2: classic
    # 3: kids
    # 4: casual
    # 5: others

    class Meta:
        db_table = "sock_category"

class SocksType(models.Model):
    title = models.CharField(max_length = 50)
    # 1: noshow
    # 2: ankle
    # 3: middle
    # 4: high
    # 5: others

    class Meta:
        db_table = "sock_type"

class PatternType(models.Model):
    title = models.CharField(max_length = 50)
    #  1: none
    #  2: Argyle
    #  3: bear
    #  4: bird
    #  5: block
    #  6: color_block
    #  7: crown
    #  8: dotted
    #  9: flower
    # 10: heart
    # 11: raindrop
    # 12: stripe
    # 13: tree
    # 14: money
    # 15: tape
    # 16: hive

    class Meta:
        db_table = "pattern_type"

class PatternDescription(models.Model):
    label         = models.CharField(max_length = 300, blank = True, null = True)
    pattern_type  = models.ForeignKey(PatternType, on_delete = models.CASCADE, default = 1)
    pattern_size  = models.IntegerField(default = 2, null = True, blank = True)
    detail_option = models.TextField(max_length = 1500, blank = True, null = True)
    # null / strip type / image url / object

    class Meta:
        db_table = "pattern_des"

class LogoType(models.Model):
    title = models.CharField(max_length = 50)
    # 1: none
    # 2: music
    # 3: moon
    # 4: nike
    # 5: mirror
    # 6: plus

    class Meta:
        db_table = "logo_type"

class LogoDescription(models.Model):
    label         = models.CharField(max_length = 300, blank = True, null = True)
    logo_type     = models.ForeignKey(LogoType, on_delete=models.CASCADE, default = 1)
    logo_size     = models.IntegerField(default = 2, null = True, blank = True)
    x_coordinate  = models.IntegerField(default = 100, null = True, blank = True)
    y_coordinate  = models.IntegerField(default = 100, null = True, blank = True)
    detail_option = models.TextField(max_length = 1500, blank = True, null = True)
    # null / image url / object

    class Meta:
        db_table = "logo_des"

class DesignDescription(models.Model):
    label        = models.CharField(max_length = 50, blank = True, null = True)
    category     = models.ForeignKey(SocksCategory, on_delete = models.CASCADE, default = 5)
    main_type    = models.ForeignKey(SocksType, on_delete = models.CASCADE, default = 5)
    color        = models.CharField(max_length = 10, default='#ffffff')
    pattern      = models.ForeignKey(PatternDescription, on_delete = models.CASCADE, default = 1)
    logo         = models.ForeignKey(LogoDescription, on_delete = models.CASCADE, default = 1)
    photo_url    = models.CharField(max_length = 5000, blank = True, null = True)
    other_req    = models.CharField(max_length = 500, blank = True, null = True)
    user         = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    wished_num   = models.IntegerField(default = 0)
    sales_volume = models.IntegerField(default = 0)
    unit_price   = models.DecimalField(blank = True, null = True, max_digits = 10, decimal_places = 2)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "design_des"
