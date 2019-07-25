from django.urls import path, include

urlpatterns = [
    path('user',include('user.urls')),
    path('product',include('product.urls')),
    path('cart',include('cart.urls')),
]
