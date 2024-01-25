from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Brand,CartItem,CustomUser,Order,Wallet,SellerWallet,AdminWallet
from  django.contrib import messages
from django.conf import settings
import razorpay

# Create your views here.
# def product(request):
#     get_pro=Product.objects.all()
#     # print(get_pro)
#     return render(request,'product.html',{'getpro':get_pro})

def category(request):
    get_cate=Category.objects.all()

    return render(request,'category.html',{'getcate':get_cate})

def subcategory(request,pk):
    get_cate=Category.objects.get(id=pk)
    get_brand= Brand.objects.filter(category_id=pk)
    content={
        'getbrand':get_brand,
        'getcate':get_cate
    }
    return render(request,'subcategory.html',content)

def viewcategory(request,pk):
    get_brand=Brand.objects.get(id=pk)
    get_pro=Product.objects.filter(brand=get_brand)
    for i in get_pro:
        i.quantity= i.quantity>0
        
    content={
        'getpro':get_pro,
        'getbrand':get_brand,
        'error':'Out of Stock'
    }
    print(get_pro)
    return render(request,'viewcategory.html',content)

def view_cart(request):
     
    try:
        user=request.user.id
    except Exception as e:
        print(e)
    cart_item=CartItem.objects.filter(user=user)
    total_price=sum(item.subtotal() for item in cart_item)
   
    print(user,cart_item,total_price)
        
    
       
    return render(request,'cart.html',{'cartitem':cart_item,'total_price':total_price})


def add_cart(request,pk):
    product=Product.objects.get(id=pk)

    cart_item,item_created=CartItem.objects.get_or_create(product=product,user=request.user)
    product.quantity-=1
    product.save()
    if not item_created:
        cart_item.quantity+=1
        cart_item.save()
        
    return redirect('category')


def remove_cart(request,pk):
    product=Product.objects.get(id=pk)
   
    cart_item=CartItem.objects.get(product=product,user=request.user)
    if cart_item.quantity>=1:
        if cart_item.quantity is not None:
            product.quantity=product.quantity+cart_item.quantity
            product.save()
        cart_item.delete()

    return redirect('cart')    
        

def increase_cart_item_quantity(request,pk):
    product=Product.objects.get(id=pk)
    cart_item=get_object_or_404(CartItem,product=product,user=request.user)

    cart_item.quantity+=1
    product.quantity-=1

    product.save()
    cart_item.save()

         
    return redirect('cart')

def decrease_cart_item_quantity(request,pk):
    product=Product.objects.get(id=pk)

    cart_item=get_object_or_404(CartItem,product=product,user=request.user)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        product.quantity=product.quantity+1
        product.save()
        cart_item.save()
    else:
        product.quantity=product.quantity+1
        product.save()
        cart_item.delete()    
    return redirect('cart')
    

def checkout(request):   
    cart_item=CartItem.objects.filter(user=request.user)
    print(cart_item)
    total_price=sum(item.subtotal() for item in cart_item)
    return render(request,'checkout.html',{'cart_item':cart_item,'total_price':total_price,})
   


def placeorder(request,pk):
    
    user=CustomUser.objects.get(id=request.user.id)
    cartitem=CartItem.objects.filter(user=request.user)
    product=get_object_or_404(Product,id=pk)
    # user=request.CustomUser.id
    print(cartitem)
    print("================",request.user.id)
    
    print(user.id)
    if request.method=='POST':
        city=request.POST['city']
       
        pincode=request.POST['pin']
        order=Order.objects.create(user_id=request.user.id,product=product,city=city,pincode=pincode)
       
        print(order)
    
    price=sum(item.subtotal() for item in cartitem)
        
    client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({'amount': price*100, "currency": "INR", 'payment_capture': 1})
    print(payment)
    order.razorpay_order_id=payment['id']
    
    cartitem.delete()
    order.save()
     

    context={'payment':payment,'total_price':price}
    return render(request,'checkout.html',context)
       
       
       
def success(request):
    user=get_object_or_404(CustomUser,id=request.user.id)
    wallet=get_object_or_404(Wallet,user=user)
    admin_user=get_object_or_404(CustomUser,email='admin@gmail.com')
    admin_wallet,created=AdminWallet.objects.get_or_create(user=admin_user)
  
    print('--------------------------')
    print(user,wallet,admin_user)
    print('--------------------------')
    order_id=request.GET.get('order_id')
    print('--------------------------')
    print(order_id)
    print('--------------------------')
    order_amount=int(request.GET.get('order_amount'))/100
   
    print('--------------------------')
    print(order_amount)
    print('--------------------------')
    
    order=Order.objects.get(razorpay_order_id=order_id)
    if user.user_type=='buyer':
       
        if wallet.balance>=order_amount:
            wallet.balance-=order_amount
            
            admin_commssion=order_amount*0.05
            admin_wallet.balance+= admin_commssion 

            
            seller = order.product.user
            print(seller)
            print("")
            seller_wallet,created=SellerWallet.objects.get_or_create(user=seller)
            seller_wallet.balance+=order_amount-admin_commssion
            seller_wallet.save()

            order.is_paid =True     
            order.save()
            wallet.save()
          
            admin_wallet.save()
            return render(request,'success.html',{'order_id':order_id})
        else:
            order.is_paid=False
            order.save()
            return render(request,'checkout.html',{'error':'Insufficient Balance'})    
    
    return render(request,'success.html',{'order_id':order_id})


def view_balance(request):
    wallet=get_object_or_404(Wallet,user=request.user)
    print("###################")
    print(wallet)
    print("###################")
    return render(request,'viewbalance.html',{'wallet':wallet})
   

