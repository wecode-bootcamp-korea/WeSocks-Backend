from django.db import models

class UserType(models.Model):
    user_type = models.CharField(max_length=20)
    class Meta:
        db_table = "user_type"

class User(models.Model):
    nickname     = models.CharField(max_length=20)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=300)
    phone_number = models.IntegerField()
    user_type    = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.CASCADE, default=1) 
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    birthday     = models.CharField(max_length=30)

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

