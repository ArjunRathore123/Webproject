from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import CustomUser
from products.models import Wallet
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def Home(request):
    return render(request,'sellerindex.html')

def sellerregister(request):
    return render(request,'sellersignup.html')

def sellerlogin(request):
    return render(request,'sellerlogin.html')

def signupform(request):
    if request.method=='POST':
        email=request.POST['email_id']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        contact=request.POST['contact']
        birthday=request.POST['birthday']
        address=request.POST['address']
        gender=request.POST['gender']
        password1=request.POST['password1']
        password2=request.POST['password2']
        user_type=request.POST['user_type']

        if password1!=password2:
            messages.error("Password and confirm password does not match")
            return redirect('home')

        user=CustomUser.objects.create_user(email=email,password=password1)
        user.first_name=first_name
        user.last_name=last_name
        user.contact=contact
        user.address=address
        user.gender=gender
        user.date_of_birth=birthday
        user.user_type=user_type
        user.save()
        
        login(request,user)
        messages.success(request,'Account Created Successfully')
        return redirect('index')
    else:
        return render(request,'sellersignup.html')


def handlelogin(request):
    if request.method=='POST':
        email=request.POST['user_login']
        password=request.POST['user_pass']
        user=authenticate(request,email=email,password=password)
        if user is not None:
            user_type=user.user_type
            print(user_type)
            if user_type=='seller':  
                login(request,user)
                return redirect('index')
            elif user_type=='buyer':
                return render(request,'sellerlogin.html',{'error':'Buyer does not login'})
        return render(request,'sellerlogin.html')

def handlelogout(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('index')

def sellerview_balance(request):
    wallet=get_object_or_404(Wallet,user=request.user)
    print("###################")
    print(wallet)
    print("###################")
    return render(request,'sellerviewbalance.html',{'wallet':wallet})
   

def sellerdeposit(request):
    
    if request.method=='POST':
        amount=request.POST['amount']
        wallet=Wallet.objects.get(user=request.user)
        print(wallet)
        wallet.balance+=int(amount)
        print("###################")
        print(wallet.balance)
        print("###################")
        wallet.save()
    return redirect('sellerviewbalance')

def sellerwithdraw(request):
  
    if request.method=='POST':
        amount=request.POST['amount']
        wallet=Wallet.objects.get(user=request.user)
        print(wallet)
        if wallet.balance>=int(amount):
            wallet.balance-=int(amount)
            print("###################")
            print(wallet.balance)
            print("###################")
            wallet.save()
            messages.success(request,f'{amount} is successfully withdrawl')
        else:
             messages.error(request,f'Insufficent Amount')
    return redirect('sellerviewbalance')