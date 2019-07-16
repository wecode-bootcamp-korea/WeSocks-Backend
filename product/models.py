from django.db import models
from django.utils import timezone

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

class PatternDescription(models.Model):
    title = models.CharField(max_length = 50)
    # 1: none
    # 2: strip
    # 3: image
    # 4: described by object
    detail_option = models.CharField(max_length = 300, blank = True, null = True)
    # null / strip type / image url / object


    class Meta:
        db_table = "pattern_des"

class LogoDescription(models.Model):
    title = models.CharField(max_length = 50)
    # 1: none
    # 2: logo_image
    # 3: described by object
    detail_option = models.CharField(max_length = 300, blank = True, null = True)
    # null / image url / object

    class Meta:
        db_table = "logo_des"

class ProductDescription(models.Model):
    category    = models.ForeignKey(SocksCategory, on_delete = models.CASCADE, default=5)
    main_type  = models.ForeignKey(SocksType, on_delete = models.CASCADE, default=5)
    color       = models.CharField(max_length=10, default='ffffff')
    pattern     = models.ForeignKey(PatternDescription, on_delete = models.CASCADE, default=1)
    logo        = models.ForeignKey(LogoDescription, on_delete = models.CASCADE, default=1)
    other_req   = models.CharField(max_length=500, blank = True, null = True)
    #designer   = models.ForeignKey(User, on_delete = models.CASCADE) => 유저 앱 기능 구현 후 추가 예정
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_des"