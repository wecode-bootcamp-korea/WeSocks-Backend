import jwt
import json
import bcrypt
import requests

from django.shortcuts     import render
from django.http          import JsonResponse, HttpResponse
from django.views         import View
from .models              import User, SocialPlatform, Address, AddressType
from .utils import login_required
from wesocks.settings import JWT_ALGORITHM
from my_settings          import jwt_key

class UserView(View):
    def post(self, request):
        new_user_info = json.loads(request.body)
       
        if User.objects.filter(email=new_user_info["email"]).exists():
            return JsonResponse({
                "error_code": "EMAIL_ALREADY_EXISTS"
            }, status=400)
        else:

            bytesd_pw = bytes(new_user_info["password"], "utf-8")
            hashed   = bcrypt.hashpw(bytesd_pw, bcrypt.gensalt())

            new_user = User(
                email        = new_user_info["email"],
                password     = hashed.decode("utf-8"),
                nickname     = new_user_info["nickname"],
                birthday     = new_user_info["birthday"],
                phone_number = new_user_info["phone_number"]
            )
            new_user.save()

            return HttpResponse(status=200)

class LoginView(View):
    def post(self, request):
      
        login_user_info  = json.loads(request.body) 
        login_user_email = login_user_info['email'] 

        if not User.objects.filter(email = login_user_email).exists():
            return JsonResponse ({"error_code": "EMAIL_NOT_EXISTS"}, status = 400)

        user = User.objects.get(email = login_user_email) 
        
        if bcrypt.checkpw(login_user_info['password'].encode('UTF-8'), user.password.encode("UTF-8")): 
            encoded_jwt = jwt.encode({'id':user.id}, jwt_key, algorithm='HS256')

            return JsonResponse({
                'access_token'   : encoded_jwt.decode('UTF-8'),
            }, status = 200)
        else:
            return JsonResponse({ "error_code": "INVALID_PASSWORD"}, status = 400) 

class UpdateView(View):

    @login_required
    def post(self, request):
        user = request.user
        login_user = json.loads(request.body)
        
        if 'nickname' in login_user:
            User.objects.filter(id=user.id).update(nickname = login_user['nickname'])

        if 'password' in login_user:
            bytesd_pw = bytes(login_user['password'], "utf-8")
            hashed = bcrypt.hashpw(bytesd_pw, bcrypt.gensalt())                                                                        
                           
            User.objects.filter(id=user.id).update(password = hashed.decode("UTF-8"))                                            
        
        if "address" in login_user:
            if Address.objects.filter(user_id=user.id).exists():
                return HttpResponse(status=200)
            else:
                Address.objects.filter(user_id=user.id).update(address = login_user["address"])
            
            new_address = Address(
                address_type = login_user["address_type"],
                address      = login_user["address"],
                recepient    = login_user["recepient"]
            )
            new_address.save()

        return HttpResponse(status=200)
 
class KakaoLoginView(View): 

    def get(self, request):
        access_token = request.headers["Authorization"]
        headers      =({'Authorization' : f"Bearer {access_token}"})
        url          = "https://kapi.kakao.com/v1/user/me"
        response     = requests.request("POST", url, headers=headers, timeout = 3)
        user         = response.json()
    
        if User.objects.filter(social_login_id = user['id']).exists(): #기존에 소셜로그인을 했었는지 확인
            user_info          = User.objects.get(social_login_id=user['id'])
            encoded_jwt        = jwt.encode({'id': user_info.id}, jwt_key, algorithm='HS256') # jwt토큰 발행
            none_member_type   = 1

            return JsonResponse({ 
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_type'    : none_member_type,
                'user_pk'      : user_info.id
            }, status = 200)            
        else:
            new_user_info = User(
                social_login_id = user['id'],
                social          = SocialPlatform.objects.get(platform ="kakao"),
                email           = user['properties'].get('email', None)
            )
            new_user_info.save()
            encoded_jwt         = jwt.encode({'id': new_user_info.id}, jwt_key, algorithm='HS256') 
            none_member_type    = 1
            
            return JsonResponse({
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_type'    : none_member_type,
                'user_pk'      : new_user_info.id,
                }, status = 200)

class NaverLoginView(View):
    
    def get(self, request):
        access_token = request.headers["Authorization"]
        headers      =({'Authorization' : f"Bearer {access_token}"})
        url          = 'https://openapi.naver.com/v1/nid/me'
        response     = requests.request("POST", url, headers=headers, timeout = 3)
        user         = response.json()
    
        if User.objects.filter(social_login_id = user['response']['id']).exists(): 
            user_info          = User.objects.get(social_login_id=user['response']['id'])
            encoded_jwt        = jwt.encode({'id': user_info.id}, jwt_key, algorithm='HS256') 
            none_member_type   = 2

            return JsonResponse({ 
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_type'    : none_member_type,
                'user_pk'      : user_info.id
            }, status = 200)            
        else:
            new_user_info = User(
                social_login_id = user['response']['id'],
                social          = SocialPlatform.objects.get(platform ="naver"),
            )
            new_user_info.save()
            encoded_jwt         = jwt.encode({'id': new_user_info.id}, jwt_key, algorithm='HS256') 
            none_member_type    = 2

            return JsonResponse({
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_type'    : none_member_type,
                'user_pk'      : new_user_info.id,
                }, status = 200)

class MypageView(View):
    
    @login_required
    def get(self, request):
        
        user_who_requested  = request.user.id
        user_object         = User.objects.values().get(pk = user_who_requested)
        requested_address = Address.objects.values().filter(pk = user_who_requested)


        return JsonResponse({
            'nickname' : user_object["nickname"],
            'reward_point' : user_object["reward_points"],
            "address_list" : list(requested_address)
        }, status=200)
