from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.forms.models import model_to_dict
from urllib import parse
from decimal import *
import json
from .models import *
from user.models import *
from cart.models import *

THUMBNAIL_DEFAULT_NUM = 3

def check_design_existence(design_des_dict):
    text_data = f"{design_des_dict['category_id']}{design_des_dict['main_type_id']}{design_des_dict['color']}{design_des_dict['pattern_type_id']}{design_des_dict['pattern_size']}{design_des_dict['logo_type_id']}{design_des_dict['logo_size']}{design_des_dict['logo_x_coordinate']}{design_des_dict['logo_y_coordinate']}"
    
    hashed_data = hash(text_data)
    
    design_descritpion_exists = DesignDescription.objects.filter(
        hash_value = hashed_data    
    ).exists()

    if design_descritpion_exists:
        existed_design = DesignDescription.objects.get(hash_value = hashed_data)

        return ({
            "check_design_exists" : design_descritpion_exists,
            "design_id"           : existed_design.id,
        })

    else:
        new_pattern = PatternDescription.objects.create(
            pattern_type  = PatternType.objects.get(id = design_des_dict["pattern_type_id"]),
            pattern_size  = design_des_dict["pattern_size"],
        )
        new_logo = LogoDescription.objects.create(
            logo_type     = LogoType.objects.get(id = design_des_dict["logo_type_id"]),
            logo_size     = design_des_dict["logo_size"],
            x_coordinate  = design_des_dict["logo_x_coordinate"],
            y_coordinate  = design_des_dict["logo_y_coordinate"],
        )
        new_design_created  = DesignDescription.objects.create(
            category   = SocksCategory.objects.get(id = design_des_dict["category_id"]),
            main_type  = SocksType.objects.get(id = design_des_dict["main_type_id"]),
            label      = design_des_dict["label"],
            color      = design_des_dict["color"],
            pattern    = new_pattern,
            logo       = new_logo,
            user       = User.objects.get(id = design_des_dict["user_pk"]),
            unit_price = design_des_dict["unit_price"]
        )
        hashed_data = hash(new_design_created)
        new_design_created.hash_value = hashed_data
        new_design_created.save()

        return ({
            "check_design_exists" : design_descritpion_exists,
            "design_id"           : new_design_created.id,
            "new_design_object"   : new_design_created
        })

class NewDesignView(View):

    def post(self, request):
        new_design_req = json.loads(request.body)
        check_design   = check_design_existence(new_design_req)

        # If the new_design_req design is a existed design>> 
        if check_design["check_design_exists"]:
            res_messange  = "existed_design"

            return JsonResponse({
                "result_message" : res_messange,
                "design_id"      : check_design["design_id"]
            }, safe = False, status = 400)
        # If the new_design_req design is the new design >> 
        else:
            new_design    = check_design["new_design_object"]
            res_message   = "design_register_success"
            pattern_data  = PatternDescription.objects.select_related('pattern_type').get(id = new_design.pattern_id)
            pattern_type  = PatternType.objects.get(id = pattern_data.pattern_type_id)
            logo_data     = LogoDescription.objects.get(id = new_design.logo_id)
            logo_type     = LogoType.objects.get(id = logo_data.logo_type_id)

        return JsonResponse({
                "result_message" : res_message,
                "general_data"   : model_to_dict(new_design),
                "pattern_type"   : pattern_type.title,
                "logo_type"      : logo_type.title,
            }
        )

class WishesReqView(View):

    def post(self, request):
        wish_req = json.loads(request.body)
        user_pk  = wish_req["user_pk"]
        
        #If Front-End does know what the design id is >>
        if "design_id" in wish_req:
            wish_design_id = wish_req["design_id"]
        # If front end does not know what the design id is >>
        else:
            check_design  = check_design_existence(wish_req)
            wish_design_id = check_design["design_id"]
 
        wished_design        = DesignDescription.objects.get(id = wish_design_id)
        check_wish_existence = WishesDetail.objects.filter(
            user_id   = wish_req["user_pk"],
            design_id = wish_design_id
            ).exists()

        if check_wish_existence:
            res_message = 'duplicate_request'
            return JsonResponse({
                "result_message": res_message,
            }, safe = False, status = 400)
        else:
            wished_design.wished_num += 1
            wished_design.save()
            new_wish = WishesDetail.objects.create(
                design = DesignDescription.objects.get(id = wish_design_id),
                user   = User.objects.get(id = wish_req["user_pk"]),
            )

            res_message  = "success"
            wished_count = DesignDescription.objects.get(id = wish_design_id).wished_num
        
            return JsonResponse({
                "result_message": res_message,
                "wished_count"  : wished_count
            }, safe = False)

class AddCartReqView(View):

    def post(self, request):
        add_cart_req = json.loads(request.body)
        #If Front-End does know what the design id is >>
        if "design_id" in add_cart_req:               
            design_id_added_to_cart = add_cart_req["design_id"]
        # If front end does not know what the design id is >>
        else: 
            check_design  = check_design_existence(add_cart_req)
            design_id_added_to_cart = check_design["design_id"]

        design_added_to_cart = DesignDescription.objects.get(id = design_id_added_to_cart)
        new_add_cart = CartDetail.objects.create(
            design        = DesignDescription.objects.get(id = design_id_added_to_cart),
            user          = User.objects.get(id = add_cart_req["user_pk"]),
            count         = add_cart_req["count"],
            total_price   = float(add_cart_req["count"]) * float(design_added_to_cart.unit_price),
            reward_points = float(add_cart_req["count"]) * float(design_added_to_cart.unit_price) * 0.1
        )
        
        if "wished_id" in add_cart_req:
            delete_wish = WishesDetail.objects.get(
                id = add_cart_req["wished_id"],
            )
            delete_wish.delete()
            res_message = "success_and_wish_canceled"
        else:
            res_message = "success"

        return JsonResponse({
            "result_message": res_message
            }, safe = False)

class CancelWishReqView(View):
    
    def post(self, request):
        cancel_wish_req = json.loads(request.body)
        check_wish_flag = WishesDetail.objects.filter(id = cancel_wish_req["wished_id"]).exists()
        
        if check_wish_flag:
            delete_wish = WishesDetail.objects.get(id = cancel_wish_req["wished_id"])
            wish_canceled_design = DesignDescription.objects.get(id = delete_wish.design_id)

            wish_canceled_design.wished_num -= 1
            wish_canceled_design.save()
            delete_wish.delete()
            
            res_message = 'wish_canceled'
            status_code = 200

        else:
            res_message = 'no_such_wished_id'
            status_code = 400 

        return JsonResponse({
            "result_message": res_message,
        }, safe = False, status = status_code)

class CancelCartReqView(View):

    def post(self, request):
        cancel_cart_req = json.loads(request.body)
        check_cart_flag = CartDetail.objects.filter(id = cancel_cart_req["cart_id"]).exists()

        if check_cart_flag:
            delete_cart = CartDetail.objects.get(id = cancel_cart_req["cart_id"])
            delete_cart.delete()
            res_message = 'cart_canceled'
            status_code = 200 
        else:
            res_message = 'no_such_cart_id'
            status_code = 400 

        return JsonResponse({
            "result_message": res_message
        }, safe = False, status = status_code)

class ChangeCartReqView(View):

    def post(self, request):
        change_cart_req = json.loads(request.body)
        check_cart_flag = CartDetail.objects.filter(id = change_cart_req["cart_id"]).exists() 

        if check_cart_flag:
            change_cart_req    = json.loads(request.body)
            cart_to_be_changed = CartDetail.objects.get(id = change_cart_req["cart_id"])          
            design_des         = cart_to_be_changed.design

            cart_to_be_changed.count         = change_cart_req["count"]
            cart_to_be_changed.total_price   = float(change_cart_req["count"]) * float(design_des.unit_price)
            cart_to_be_changed.reward_points = float(change_cart_req["count"]) * float(design_des.unit_price) * 0.1
            cart_to_be_changed.save()

            res_message = "cart_changed"
            status_code = 200
        
        else:
            res_message = "no_such_cart_id"
            status_code = 400 

        return JsonResponse({
            "result_message": res_message,
        }, safe = False, status = status_code)

class MostWishedProductView(View):

    def post(self, request):
        post_num = int(request.GET.get('num', THUMBNAIL_DEFAULT_NUM))
        
        most_wished_list_req = json.loads(request.body)
        most_wished_products = list(
            DesignDescription.objects.filter(
                main_type_id = most_wished_list_req["main_type"]
                ).order_by("-wished_num").values(
                    'label', 
                    'category_id',
                    'main_type_id',
                    'color',
                    'pattern_id',
                    'logo_id',
                    'photo_url',
                    'other_req',
                    'user_id',
                    'wished_num',
                    'sales_volume',
                    'unit_price'
                )[:post_num])
        
        return JsonResponse(most_wished_products, safe = False)