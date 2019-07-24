import json

from django.test import TestCase
from django.test import Client

from .models import *

class UserTest(TestCase):

    def test_change_address(self):
        c = Client()

        UserType.objects.create(
            user_type = "test_user_type"
        )

        User.objects.create(
            nickname     = "test_nickname",
            email        = "test_email@gmail.com",
            password     = "test_password",
            phone_number = 1012341234,
            user_type    = UserType.objects.get(user_type = "test_user_type"),
            created_at   = "2019-07-24 04:41:02.765135",
            updated_at   = "2019-07-24 04:41:02.765135",
            birthday     = "test_birthday"
        )      

        AddressType.objects.create(
            address_type = "test_address_type"
        )

        test = {
            "id"           : 1,
            "user"         : User.objects.get(email = "test_email@gmail.com").id, 
            "address_type" : AddressType.objects.get(address_type = "test_address_type").id, 
            "address"      : "test_address",
            "recepient"    : "test_recepient"
        } 
        
        response = c.post(
            "/user/address",
            test,
            content_type="application/json"
        ) 

        self.assertEqual = (response.status_code, 200)
