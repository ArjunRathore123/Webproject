from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serilaizers import SellerLoginSerialzier,SellerRegisterSerializer
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class SellerRegisterView(APIView):
    def post(self,request,*args,**kwargs):
        try:
            user=request.user.id
            buyer_account=CustomUser.objects.filter(id=user).exists()
            if buyer_account:
                
                serializer=SellerRegisterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    context={
                        'success':True,
                        'status':status.HTTP_201_CREATED,
                        'msg':'Registration Successful',
                        'data':serializer.data
                    }
                    return Response(context)
                context={
                        'success':False,
                        'status':status.HTTP_400_BAD_REQUEST,
                        'msg':'Invalid Crediancial',
                        'data':serializer.errors
                    }
                return Response(context)
            return Response({"error": "You cannot create a seller account as you already have a buyer account."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context={
                    'success':False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'Invalid Crediancial',
                    'data':str(e)
                }
            return Response(context)
        
       
class SellerLoginView(APIView):
    def post(self, request): 
        try:
            serializer=SellerLoginSerialzier(data=request.data)
            if serializer.is_valid():
                email=serializer.data['email']
                password=serializer.data['password']
               
                user=authenticate(email=email,password=password)
                
                if user:
                    if user.user_type=='seller' or user.user_type=='Seller':
                        refresh = RefreshToken.for_user(user)

                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        })
                  
                    return Response({
                        'success':False,
                        'status':status.HTTP_401_UNAUTHORIZED,
                        'msg':'Login Falied. User is not buyer',
                        'data':serializer.data
                    })
                
            
                return Response({
                        'success':False,
                        'status':status.HTTP_401_UNAUTHORIZED,
                        'msg':'Invalid Credentials',
                        'data':serializer.errors
                    })
            
            return Response({
                        'success':False,
                        'status':status.HTTP_400_BAD_REQUEST,
                        'msg':'Login Failed',
                        'data':serializer.errors
                    })
        except Exception as e:
            context={
                    'success':False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'Invalid Crediancial',
                    'data':str(e)
                }
            return Response(context)
        

        
    
