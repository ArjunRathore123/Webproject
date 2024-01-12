from.views import sellerlogin,sellerregister,Home,handlelogin,handlelogout,signupform,sellerview_balance,sellerdeposit,sellerwithdraw
from django.urls import path

urlpatterns = [
  path('index/',Home,name='index'),
  path('signup/',sellerregister,name='sellerregister'),
  path('signin/',sellerlogin,name='sellerlogin'),
  path('sellersignup',signupform,name='signup'),
  path('sellerlogin',handlelogin,name='handlelogin'),
  path('logout',handlelogout,name='handlelogout'),
  path('sellerviewbalance/',sellerview_balance,name='sellerviewbalance'),
  path('sellerdeposit/',sellerdeposit,name='sellerdeposit'),
  path('sellerwithdraw/',sellerwithdraw,name='sellerwithdraw'),

 
]
