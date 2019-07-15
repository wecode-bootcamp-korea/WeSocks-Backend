from django.urls import path
from . import views
from .views import user_test

urlpatterns = [
        path('/test',views.user_test),
        ]        
