from django.db import models

class UserType(models.Model):

    user_type = models.CharField(max_length=20)
    
    class Meta:
        db_table = "user_type"

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20)

    class Meta:
        db_table = "social_platform"

class User(models.Model):
    
    nickname     = models.CharField(max_length=20)
    email        = models.EmailField(max_length=50, unique=True, null=True)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=12)
    user_type    = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.SET_NULL)
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, null=True)
    social_login_id = models.CharField(max_length=50, blank=True) 
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    birthday        = models.DateTimeField(null=True, blank=True)
    reward_points    = models.DecimalField(blank = True, null = True, max_digits = 10, decimal_places = 4)

    class Meta:
        db_table = "user"

class AddressType(models.Model):
    address_type = models.CharField(max_length=20)

    class Meta:
        db_table = "address_type_list"

class Address(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.OneToOneField(AddressType, on_delete=models.CASCADE, primary_key=True)
    address      = models.CharField(max_length=100)
    recepient    = models.CharField(max_length=20)

    class Meta:
        db_table = "address"

