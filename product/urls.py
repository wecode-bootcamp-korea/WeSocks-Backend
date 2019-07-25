from django.urls import path
from . import views
from .views import *

urlpatterns = [
        path('/new_design', NewDesignView.as_view()),
        path('/wish_req', WishesReqView.as_view()),
        path('/add_cart_req', AddCartReqView.as_view()),
        path('/cancel_wish_req', CancelWishReqView.as_view()),
        path('/cancel_cart_req', CancelCartReqView.as_view()),
        path('/change_cart_req', ChangeCartReqView.as_view()),
        path('/most_wished', MostWishedProductView.as_view()),
]
