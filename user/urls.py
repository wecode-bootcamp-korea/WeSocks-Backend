from django.urls import path
from . import views
from .views import UserView, LoginView, AddressView, UpdateAddressView

urlpatterns = [
    path('',UserView.as_view()),
    path('/login',LoginView.as_view()),
    path('/address/<int:requested_user_id>', AddressView.as_view()),
    path('/address/update',UpdateAddressView.as_view()),
]        
