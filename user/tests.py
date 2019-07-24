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
            id           = 1,
            nickname     = "test_nickname",
            email        = "test_email@gmail.com",
            password     = "test_password",
            phone_number = 1012341234,
            user_type    = UserType.objects.get(user_type = "test_user_type"),
            created_at   = "2019-07-24 04:41:02.765135",
            updated_at   = "2019-07-24 04:41:02.765135",
            birthday     = "1960-07-24 04:41:02.123124"
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
            "/user/address/update",
            test,
            content_type = "application/json"
        ) 

        self.assertEqual = (response.status_code, 200)

    def test_address(self):
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
            birthday     = "1960-07-24 04:41:02.123124"
        )

        AddressType.objects.create(
            address_type = "test_address_type"
        )

        response = c.get(
                "/user/address/1",
                content_type = "application/json"
        ) 

        test_address = Address.objects.create(
            user         = User.objects.get(pk = 1),
            address_type = AddressType.objects.get(address_type = "test_address_type"),
            address      = "test_address",
            recepient    = "test_recepient"
        )

        self.assertEqual = (response.status_code, 200)
        self.assertEqual = (response.json(), {"address_list": test_address})

