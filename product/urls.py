from django.urls import path
from . import views
from .views import product_test

urlpatterns = [
        path('/test',views.product_test),
        ]        
