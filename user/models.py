from django.db import models


class UserType(models.Model):
    user_type = models.CharField(max_length=20)
    class Meta:
        db_table = "user_type"

#class SocialPlantform(models.Model):
    #platform = models.CharField(max_length=30, default=0)

    #class Meta:
        #db_table = "social_platform"


class User(models.Model):
    nickname     = models.CharField(max_length=20)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=300)
    phone_number = models.IntegerField()
    user_type = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.CASCADE, default=1) 
    #social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    #social_login_id = models.CharField(max_length=50, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    birthday        = models.CharField(max_length=30)


    class Meta:
        db_table = "user"
