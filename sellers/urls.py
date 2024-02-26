from.views import sellerlogin,sellerregister,Home,handlelogin,handlelogout,signupform,sellerview_balance,sellerdeposit,sellerwithdraw
from django.urls import path

urlpatterns = [
  path('index/',Home,name='index'),
  path('signup/',sellerregister,name='sellerregister'),
  path('signin/',sellerlogin,name='sellerlogin'),
  path('sellersignup',signupform,name='sellersignup'),
  path('sellerlogin',handlelogin,name='sellerhandlelogin'),
  path('logout',handlelogout,name='sellerhandlelogout'),
  path('sellerviewbalance/',sellerview_balance,name='sellerviewbalance'),
  path('sellerdeposit/',sellerdeposit,name='sellerdeposit'),
  path('sellerwithdraw/',sellerwithdraw,name='sellerwithdraw'),

 
]
