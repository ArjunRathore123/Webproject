from django.urls import path,include
from .views import ProductView,SellerProductView,AddtoCartView,RemoveCartView,IncreaseCartItemView,DecreaseCartItemView,CreateOrderView,PaymentSuccessView,OrderCancelView

urlpatterns = [
   path('product/',ProductView.as_view(),name='showproduct'),
   path('product/',ProductView.as_view(),name='addproduct'),
   path('product/',ProductView.as_view(),name='productupdate'),
   path('product/',ProductView.as_view(),name='productdelete'),
   path('product/',SellerProductView.as_view(),name='sellerproduct'),
   path('addtocart/',AddtoCartView.as_view(),name='add_to_cart'),   
   path('removefromcart/',RemoveCartView.as_view(),name='removefromcart'),
   path('increasecartitem/',IncreaseCartItemView.as_view(),name='increasecartitem'),
   path('decreasecartitem/',DecreaseCartItemView.as_view(),name='decreasecartitem'),
   path('placeorder/',CreateOrderView.as_view(),name='placeorder'),
   path('orderpaid/',PaymentSuccessView.as_view(),name='paid'),
   path('ordercancel/',OrderCancelView.as_view(),name='ordercancel')
]