import jwt
import json
from my_settings import jwt_key
from .models import User
from django.http import JsonResponse, HttpResponse


def login_required(f):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        
        if access_token == None:
            return JsonResponse({"message" : "로그인이 필요한 서비스입니다."}, status=401)
        else:
           
            decode = jwt.decode(access_token, jwt_key, algorithms=['HS256'])
            user_id = decode["id"]
            user = User.objects.get(id=user_id)
            request.user = user

            return f(self, request, *args, **kwargs)

    return wrapper