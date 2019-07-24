from django.urls import path
from . import views
from .views import UserView, LoginView, ChangeAddressView

urlpatterns = [
    path('',UserView.as_view()),
    path('/login',LoginView.as_view()),
    path('/address',ChangeAddressView.as_view())
]        
