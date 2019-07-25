import json
import unittest
import bcrypt

from user.models import User, UserType, SocialPlatform, Address, AddressType
from unittest.mock import patch, MagicMock
from django.test import Client
from django.test import TestCase

class UserTest(TestCase):

    def setUp(self):

        model_social = SocialPlatform.objects.create(
            platform= 'kakao'
        )
        model_type = UserType.objects.create(
            user_type= "normal_user" 
        )
        bytesd_pw = bytes('1234', 'utf-8')
        hashed = bcrypt.hashpw(bytesd_pw, bcrypt.gensalt())
        
        User.objects.create(
            email = 'admin@gmail.com',
            nickname ="운영자",
            password =hashed.decode('UTF-8'),
            phone_number = "01012341234",
            birthday = "2019-07-24",
            user_type = model_type,
            social = model_social
        )

    def tearDown(self):
        User.objects.filter(email='test').delete()       

    def test_user_signup(self):
        c = Client()

        test = {
            'email' : 'admin1@gmail.com',
            'nickname':'test1',
            'password':'1234',
            'phone_number' : "01012341234",
            'birthday' : "2019-07-24"
            }
        response     = c.post('/user', json.dumps(test), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        c = Client()

        test         = {'email':'admin@gmail.com', 'password':'1234'}
        user         = User.objects.get(email=test['email'])
        response     = c.post('/user/login', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.json(), 
                    {
                        "access_token" : access_token
                    }
        )
        
    def test_user_nickname_update(self):
        c = Client()

        test         = {"email":"admin@gmail.com", "password":"1234"}
        response     = c.post("/user/login", json.dumps(test), content_type="application/json")
        access_token = response.json()["access_token"]

        test     = {"nickname":"testnick2"}
        response = c.post(
            "/user/update",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":access_token,"content_type":"application/json"}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_password_update(self):
        c = Client()

        test         = {"email":"admin@gmail.com", "password":"1234"}
        response     = c.post("/user/login", json.dumps(test), content_type="application/json")
        access_token = response.json()["access_token"]

        test     = {"password":"12345"}
        response = c.post(
            "/user/update",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":access_token, "content_type":"application/json"}
        )
        self.assertEqual(response.status_code, 200)
    
