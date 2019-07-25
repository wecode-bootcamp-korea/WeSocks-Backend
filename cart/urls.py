from django.urls import path
from . import views
from .views import *

urlpatterns = [
        path('/wishes', MyWishesView.as_view()),
        path('/list', MyCartView.as_view()),
]
