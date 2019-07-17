import jwt
import json
import bcrypt
import requests

from django.shortcuts     import render
from django.http          import JsonResponse, HttpResponse
from django.views         import View
from .models              import User
from my_settings          import jwt_key
from wesocks.settings import JWT_ALGORITHM

class UserView(View):
    def post(self, request):
        new_user_info = json.loads(request.body)
       
        if User.objects.filter(email=new_user_info["email"]).exists():
            return JsonResponse({
                "error_code": "EMAIL_ALREADY_EXISTS"
            }, status=400)
        else:
            password = bytes(new_user_info["password"], "utf-8")
            hashed   = bcrypt.hashpw(password, bcrypt.gensalt())

            new_user = User(
                nickname     = new_user_info["nickname"],
                password     = hashed.decode("utf-8"),
                email        = new_user_info["email"],
                phone_number = new_user_info["phone_number"],
                birthday     = new_user_info["birthday"]
            )

            new_user.save()

            return JsonResponse(status=200)

class LoginView(View):
    def post(self, request):
      
        login_user_info  = json.loads(request.body) 
        login_user_email = login_user_info['email'] 

        if not User.objects.filter(email = login_user_email).exists():
            return JsonResponse ({"error_code": "EMAIL_NOT_EXISTS"}, status = 400)

        user = User.objects.get(email = login_user_email) 
        
        if bcrypt.checkpw(login_user_info['password'].encode('UTF-8'), user.password.encode("UTF-8")): 
            encoded_jwt = jwt.encode({'email':email}, wef_key, algorithm='HS256')

            return JsonResponse({
                'access_token'   : encoded_jwt.decode('UTF-8'),
            }, status = 200)
        else:
            return JsonResponse({ "error_code": "INVALID_PASSWORD"}, status = 400)