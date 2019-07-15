from django.urls import path
from . import views
from .views import main_test

urlpatterns = [
        path('/test',views.main_test),
        ]        
