from django.views import View
from django.http import JsonResponse,HttpResponse
import json

def product_test(request):
    return HttpResponse("<h1>테스트</h1>")