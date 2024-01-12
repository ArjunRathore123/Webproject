from django.contrib import admin
from .models import Product,Category,Color,Brand,CartItem,Order,Wallet,SellerWallet,AdminWallet
# Register your models her.
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','product_name','category','brand','product_image','price','quantity','description')
    fieldsets=((None,{"fields":('product_image','category','brand','product_name','color','price','quantity','description')}),)
    add_fieldsets=(
        (None,{'classes':("wide",),
               'fields':('product_image','category','brand','product_name','color','price','quantity','description')},
        )
    )
    search_fields=('product_name',)
    ordering=('product_name',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(CartItem)
admin.site.register(Wallet)
admin.site.register(SellerWallet)
admin.site.register(AdminWallet)
admin.site.register(Order)
