from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
from urllib import parse
import json

from .models import SocksCategory, SocksType, PatternType, PatternDescription, LogoType, LogoDescription, DesignDescription


def product_test(request):
    return HttpResponse("<h1>테스트</h1>")

class NewDesignView(View):

    def post(self, request):

        new_design      = json.loads(request.body)
        print(new_design)
        new_design_data = DesignDescription.objects.create(
            label       = new_design["label"],
            category_id = new_design["category"],
            main_type_id= new_design["main_type"],
            color       = new_design["color"],
            pattern_id  = new_design["pattern"],
            logo_id     = new_design["logo"],
            other_req   = new_design["other_req"],
            # designer    = new_design["designer"],
            )
        new_design_data.save()
        message = "register_success"

        return JsonResponse({
            "message"       : message,
            "design_id"     : new_design_data.id,
            "design_label"  : new_design_data.label,
            }
        )