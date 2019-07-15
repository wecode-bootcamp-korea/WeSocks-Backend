from django.urls import path, include

urlpatterns = [
    path('user',include('user.urls')),
    path('product',include('product.urls')),
    path('mypage',include('mypage.urls')),
    path('main',include('main.urls')),
]
