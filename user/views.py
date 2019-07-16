
import json

import bcrypt
import requests

from django.shortcuts     import render
from django.http          import JsonResponse, HttpResponse
from django.views         import View
from .models              import User



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
                phone_number = new_user_info["phone_number"]
            )

            new_user.save()

            return JsonResponse({"message" : "Thanks your account has been successfully created."}, status=200)