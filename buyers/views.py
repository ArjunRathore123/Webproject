from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import CustomUser
from django.http import HttpResponse
from django.contrib.auth import login ,logout,authenticate
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


def Home(request):
    return render(request,'index.html')

def account(request):
    return render(request,'account.html')

def Register(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'login.html')


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
        return render(request,'signup.html',{'success':'Account Created Successfully'})
    else:
        return render(request,'signup.html')


def handlelogin(request):
    if request.method=='POST':
        email=request.POST['user_login']
        password=request.POST['user_pass']
        user=authenticate(request,email=email,password=password)
        if user is not None:
            user_type=user.user_type
            print(user_type)
            if user_type=='buyer':  
                login(request,user) 
                return redirect('home')
            elif user_type=='seller':     
                return render(request,'login.html',{'error':'Seller doesnot login'})
        return render(request,'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('home')

def contactus(request):
    return render(request,'contactus.html')

def send_email(request):
    if request.method=="POST": 
       email=request.POST['email']
       subject=request.POST['subject']
       name=request.POST.get('name','')
       mobile_number=request.POST.get('number','')
       msg=request.POST['message']
       message=f'Name:{name}\nMobile Number:{mobile_number}\n{email}\n{msg}'
       send_mail(subject,message,email,[settings.EMAIL_HOST_USER],fail_silently=True)
    
       message=f"Hey {name},\nThanks for the enquiry we have received it,\nI am Arjun Rathore. I'm here to welcoming you on behalf of Infograins, I'm a sales director and a founder of Infograins, we will be in touch with you shortly, In a meantime if you have any questions or requirement detail you can revert on this email itself so that based on it we can quickly schedule our discussion or conversation on it.Also, you can schedule a meeting to discuss your specific requirements, here is the calendly link, kindly book your slot as per your convenience, so that we can connect with you to have a more precise conversation regarding your requirement."
       send_mail("Thank you for contact Flipkart",
                 message,
                 settings.EMAIL_HOST_USER,
                 [email],
                 fail_silently=False)

       print(email)

       messages.success(request,"Message sent successfully")
       return render(request,"contactus.html")
    else:
       messages.error(request,"Message not sent ")
       return render(request,"contactus.html")