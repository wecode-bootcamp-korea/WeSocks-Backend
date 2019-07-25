from django.urls import path
from . import views


from .views import UserView, LoginView, UpdateView, KakaoLoginView, NaverLoginView

urlpatterns = [
        path('',UserView.as_view()),
        path('/login',LoginView.as_view()),
        path('/login/kakao',KakaoLoginView.as_view()),
        path('/login/naver',NaverLoginView.as_view()),
        path('/update', UpdateView.as_view())
]