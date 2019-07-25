import json
import bcrypt
import requests

from django.test import TestCase
from django.test import Client

from user.models import *
from product.models import *
from cart.models import *


class ProductAppTest(TestCase):

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
            unit_price  = 8000, 
            other_req   = "Born again.",
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
            unit_price  = 9000, 
            other_req   = "Born again."
        )
        design2.save()

        # 마이 위시 data 생성
        wish1 = WishesDetail.objects.create(
            id      = 1,
            user    = tester1,
            label   = "test_wish",
            design  = design1,
        )
        wish1.save()

        # 마이 카트 data 생성
        cart1 = CartDetail.objects.create(
            id      = 1,
            user    = tester1,
            label   = "test_cart",
            design  = design1,
            count  = 1
        )
        cart1.save()

    def test_new_design_req(self):
        c = Client()
        test = {
            "user_pk"       : "1",
            "label"         : "new_design",
            "category_id"   : "1",
            "main_type_id"  : "1",
            "color"         : "#111111",
            "pattern_id"    : "1",
            "logo_id"       : "1",
            "other_req"     : "Born again",
            "unit_price"    : 10000
        }   
        response = c.post(
            "/product/new_design", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result_message": "design_register_success",
                "general_data": {
                    "id": 3,
                    "label": "new_design",
                    "category": 1,
                    "main_type": 1,
                    "color": "#111111",
                    "pattern": 1,
                    "logo": 1,
                    "photo_url": None,
                    "other_req": None,
                    "user": 1,
                    "wished_num": 0,
                    "sales_volume": 0,
                    "unit_price": 10000
                },
                "pattern_type": "none",
                "logo_type": "none"
            }
        )

    def test_duplicated_wishes_req(self):
        c = Client()
        test = {
            "user_pk"   : "1",
            "design_id" : "1"
        }
        response = c.post(
            "/product/wish_req", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "result_message": "duplicate_request"
            }
        )

    def test_first_wishes_req(self):
        c = Client()
        test = {
            "user_pk"   : "1",
            "design_id" : "2"
        }
        response = c.post(
            "/product/wish_req", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result_message": "success",
                "wished_count": 1
            }
        )

    def test_add_cart_req(self):
        c = Client()
        test = {
            "user_pk"	: "1",
            "design_id"	: "2",
            "count"	: "3"
        }
        response = c.post(
            "/product/add_cart_req", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result_message": "success"
            }
        )

    def test_cancel_wish_req(self):
        c = Client()
        test = {
	    "wished_id" : "1"
        }
        response = c.post(
            "/product/cancel_wish_req", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result_message": "wish_canceled"
            }
        )

    def test_cancel_cart_req(self):
        c = Client()
        test = {
	    "cart_id" : "1"
        }
        response = c.post(
            "/product/cancel_cart_req", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result_message": "cart_canceled"
            }
        )

    def test_change_cart_req(self):
        c = Client()
        test = {
	        "cart_id" : "1",
            "count"  : "10"  
        }
        response = c.post(
            "/product/change_cart_req", 
            json.dumps(test), 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        cart1 = CartDetail.objects.get(id = 1)
        self.assertEqual(cart1.count, 10)
        self.assertEqual(
            response.json(),
            {
                "result_message": "cart_changed"
            }
        )
    
    def test_most_wish(self):
        c = Client()
        test = {
	        "main_type" : "1",
        }
        response = c.post(
            "/product/most_wished", 
            json.dumps(test), 
            content_type = "application/json"
        )
        most_wished_products = list(
            DesignDescription.objects.filter(
                main_type_id = 1
            ).order_by("-wished_num").values()[:3])
        print("여기를 찍어요")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),[{
                'label': 'test_design1', 
                'category_id': 1, 
                'main_type_id': 1, 
                'color': '#aaaaaa', 
                'pattern_id': 1, 
                'logo_id': 1, 
                'photo_url': None, 
                'other_req': 'Born again.', 
                'user_id': 1, 'wished_num': 1, 
                'sales_volume': 0, 
                'unit_price': '8000.00'
            }]        )
    
