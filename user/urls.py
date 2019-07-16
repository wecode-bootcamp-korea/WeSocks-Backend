from django.urls import path
from . import views
from .views import UserView

urlpatterns = [
        path('',UserView.as_view()),
        ]        
