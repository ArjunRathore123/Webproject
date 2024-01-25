from.views import category,subcategory,viewcategory,view_cart,add_cart,remove_cart,decrease_cart_item_quantity,increase_cart_item_quantity,success,checkout,placeorder,view_balance
from django.urls import path

urlpatterns = [
     
        path('category/',category,name='category'),
        path('subcategory/<int:pk>',subcategory,name='brand'),
        path('viewcategory/<int:pk>',viewcategory,name='viewcategory'),
        path('add-to-cart/<int:pk>/', add_cart, name='add-to-cart'),
        path('remove-from-cart/<int:pk>/', remove_cart, name='remove-from-cart'),
        path('cart/', view_cart, name='cart'),
        path('increase_cart_item_quantity/<int:pk>/', increase_cart_item_quantity, name='increase_cart_item_quantity'),
        path('decrease_cart_item_quantity/<int:pk>/', decrease_cart_item_quantity, name='decrease_cart_item_quantity'),
        path('success/', success, name='success'),
        path('checkout/',checkout,name='checkout'),
        path('placeorder/<int:pk>',placeorder,name='place-order'),
        path('viewbalance/',view_balance,name='viewbalance'),     
       
]
