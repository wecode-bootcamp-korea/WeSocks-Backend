import json
import bcrypt
import requests
from django.test import TestCase
from django.test import Client
from user.models import *
from product.models import *
from cart.models import *

class MyPageAppTest(TestCase):

    def setUp(self):

        model_type = UserType.objects.create(user_type = "normal_user")
        tester1 = User.objects.create(
            id           = 1,
            email        = "admin1@gmail.com",
            nickname     = "tester1",
            password     = "1234",
            phone_number = "163",
            birthday     = "00001225",
            user_type    = model_type,
        )  
        tester2 = User.objects.create(
            id           = 2,                
            email        = "admin2@gmail.com",
            nickname     = "tester2",
            password     = "1234",
            phone_number = "163",
            birthday     = "00001225",
            user_type    = model_type,
        )  
        # 양말 디자인 data 생성
        s_category     = SocksCategory.objects.create(id = 1, title = "athletic")
        s_type1        = SocksType.objects.create(id = 1, title = "noshow")
        s_type2        = SocksType.objects.create(id = 2 ,title = "ankle")
        s_pattern_type = PatternType.objects.create(id = 1, title = "none")
        s_pattern_des  = PatternDescription.objects.create(id = 1, pattern_type = s_pattern_type)
        s_logo_type    = LogoType.objects.create(id = 1, title = "none")
        s_logo_des     = LogoDescription.objects.create(id = 1, logo_type = s_logo_type)
        
        design1 = DesignDescription.objects.create(
            id          = 1,
            label       = "test_design1", 
            category    = s_category,
            main_type   = s_type1,
            pattern     = s_pattern_des,
            logo        = s_logo_des,
            color       = "#aaaaaa",
            user        = tester1,
            unit_price  = "8000", 
            other_req   = "Born again.",
            photo_url   = "test.photo1.com",
            wished_num  = 1
        )
        design1.save()
        design2 = DesignDescription.objects.create(
            id          = 2,             
            label       = "test_design2",
            category    = s_category,
            main_type   = s_type2,
            pattern     = s_pattern_des,
            logo        = s_logo_des,
            color       = "#bbbbbb",
            user        = tester2,
            unit_price  = "9000", 
            other_req   = "Born again.",
            photo_url   = "test.photo2.com",
            wished_num  = 1
        )
        design2.save()

        # 마이 위시 data 생성
        wish1 = WishesDetail.objects.create(
            id         = 1,
            user       = tester1,
            label      = "test_wish",
            design     = design1,
        )
        wish1.created_at = "2019-07-20 23:59:59"
        wish1.save()

        # 마이 카트 data 생성
        cart1 = CartDetail.objects.create(
            id            = 1,
            user          = tester1,
            label         = "test_cart",
            design        = design1,
            count         = 1,
            total_price   = 8000,
            reward_points = 800

        )
        cart1.created_at = "2019-07-20 23:59:59"
        cart1.save()     

    def test_my_wishes(self):
        c = Client()
        test = {"user_pk": "1"}
        response = c.post(
                "/cart/wishes", 
                json.dumps(test), 
                content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "user_pk"      : "1",
                "my_wish_list" : [{
                    "id"            : 1,
                    "my_wish_label" : "test_wish",
                    "wished_date"   : "2019-07-20T14:59:59Z",
                    "design": {
                        "id"          : 1,
                        "label"       : "test_design1",
                        "category"    : 1,
                        "main_type"   : 1,
                        "color"       : "#aaaaaa",
                        "pattern"     : 1,
                        "logo"        : 1,
                        "photo_url"   : "test.photo1.com",
                        "other_req"   : "Born again.",
                        "user"        : 1,
                        "wished_num"  : 1,
                        "sales_volume": 0,
                        "unit_price"  : "8000.00"
                    }
                }]
            }
        )

    def test_my_cart(self):
        c = Client()
        test = {"user_pk": "1"}
        response = c.post(
                "/cart/list", 
                json.dumps(test), 
                content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "user_pk": "1",
                "my_cart_total_price": "8000.00",
                "my_cart_total_count": 1,
                "my_total_points": "800.00",
                "my_cart_list": [{
                    "id": 1,
                    "add_cart_date": "2019-07-20T14:59:59Z",
                    "count": 1,
                    "total_price": "8000.00",
                    "reward_points": "800.00",
                    "design": {
                        "id": 1,
                        "label": "test_design1",
                        "category": 1,
                        "main_type": 1,
                        "color": "#aaaaaa",
                        "pattern": 1,
                        "logo": 1,
                        "photo_url": "test.photo1.com",
                        "other_req": "Born again.",
                        "user": 1,
                        "wished_num": 1,
                        "sales_volume": 0,
                        "unit_price": "8000.00"
                    }
                }]
            }
        )