from .views import BuyerRegisterView,BuyerLoginView,ForgetPasswordView,ChangePasswordView
from django.urls import path


urlpatterns = [
    path('register/',BuyerRegisterView.as_view(),name='buyerregister'),
    path('login/',BuyerLoginView.as_view(),name='buyerlogin'),
    path('forget-password/',ForgetPasswordView.as_view(),name='forgetpassword'),
    path('reset-password/',ChangePasswordView.as_view(),name='changepassword'),
]