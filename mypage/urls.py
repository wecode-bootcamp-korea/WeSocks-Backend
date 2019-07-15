from django.urls import path
from . import views
from .views import mypage_test

urlpatterns = [
        path('/test',views.mypage_test),
        ]        
