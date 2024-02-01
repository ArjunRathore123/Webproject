from .views import Home,Register,signin,signupform,handlelogin,handlelogout,contactus,send_email
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',Home,name='home'),
    path('register/',Register,name='register'),
  
    path('login/',signin,name='login'),
    path('signup',signupform,name='signup'),
    path('login',handlelogin,name='handlelogin'),
    path('logout',handlelogout,name='handlelogout'),
    path('send_email/', send_email,name='sendemail'),
    path('contactus/',contactus,name='contactus'),
    path('contactus/sendemail',send_email,name='sendemail'),
]

if settings.DEBUG:
  urlpattern += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
  urlpattern += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
