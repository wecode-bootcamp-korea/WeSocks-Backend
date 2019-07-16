from django.urls import path
from . import views
from .views import product_test, NewDesignView

urlpatterns = [
        path('/test',views.product_test),
        path('/new_design', NewDesignView.as_view()),
        ]
