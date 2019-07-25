import json
from django.views import View
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.forms.models import model_to_dict
from urllib import parse
from django.http import JsonResponse,HttpResponse
from django.db import models
from django.utils import timezone
from django.db.models import F, Sum, Count, Case, When
from .models import *
from user.models import *
from product.models import *

class MyWishesView(View):

    def post(self, request):
        wish_list_req   = json.loads(request.body)
        my_wish_list    = {
            'user_pk'       : wish_list_req["user_pk"],
            'my_wish_list'  :[{
                'id'            :   wishes_detail["id"],
                'my_wish_label' :   wishes_detail["label"],
                'wished_date'   :   wishes_detail["created_at"],
                'design'        :   model_to_dict(DesignDescription.objects.get(id = wishes_detail["design_id"]))
            } for wishes_detail in WishesDetail.objects.filter(user_id = wish_list_req["user_pk"]).values()]
        }

        return JsonResponse(my_wish_list, safe = False)

class MyCartView(View):

    def post(self, request):
        cart_list_req    = json.loads(request.body)
        user_pk          = cart_list_req["user_pk"]
        my_cart_overview = CartDetail.objects.filter(user_id = cart_list_req["user_pk"]).aggregate(
            estimate_cost = Sum("total_price"),
            total_count   = Sum("count"),
            total_points  = Sum("reward_points")
        )

        my_cart_list  = {
            'user_pk'              : cart_list_req["user_pk"],
            'my_cart_total_price'  : my_cart_overview["estimate_cost"],
            'my_cart_total_count'  : my_cart_overview["total_count"],
            'my_total_points'      : my_cart_overview["total_points"],
            'my_cart_list'  :[{
                'id'            :   cart_detail["id"],
                'add_cart_date' :   cart_detail["created_at"],
                'count'         :   cart_detail["count"],
                'total_price'   :   cart_detail["total_price"],
                'reward_points' :   cart_detail["reward_points"],
                'design'        :   model_to_dict(
                    DesignDescription.objects.select_related('pattern').get(id = cart_detail["design_id"])
                )
            }for cart_detail in CartDetail.objects.filter(user_id = cart_list_req["user_pk"]).values()]
        }

        return JsonResponse(my_cart_list, safe = False)
