from .views import SellerLoginView,SellerRegisterView
from django.urls import path
from . import views

urlpatterns = [
    path('register/',SellerRegisterView.as_view(),name='sellerregister'),
    path('login/',SellerLoginView.as_view(),name='sellerlogin'),
    
]