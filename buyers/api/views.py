from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serilaizers import BuyerRegisterSerializer,BuyerLoginSerialzier,ForgetPasswordSerializer,ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError

class BuyerRegisterView(APIView):
    def post(self,request):
        try:
            serializer=BuyerRegisterSerializer(data=request.data)
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
        except Exception as e:
            context={
                    'success':False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'Invalid Crediancial',
                    'data':str(e)
                }
            return Response(context)
       
class BuyerLoginView(APIView):
    def post(self, request): 
        try:
            serializer=BuyerLoginSerialzier(data=request.data)
            if serializer.is_valid():
                email=serializer.data['email']
                password=serializer.data['password']
               
                user=authenticate(email=email,password=password)
                
                if user:
                    if user.user_type=='buyer' or user.user_type=='Buyer':
                        refresh = RefreshToken.for_user(user)

                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        })
                  
                    return Response({
                        'success':False,
                        'status':status.HTTP_401_UNAUTHORIZED,
                        'msg':'Login Falied. User is not buyer',
                        'data':{}
                    })
                
            
                return Response({
                        'success':False,
                        'status':status.HTTP_401_UNAUTHORIZED,
                        'msg':'Invalid Credentials',
                        'data':{}
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
            

class ForgetPasswordView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        serializer=ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'detail': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            token=default_token_generator.make_token(user)
            reset_link=f"http://127.0.0.1:8000/buyerApi/reset-password/?user_id={user.id}&token={token}"
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                email,
                [email],
                fail_silently=False,
            )
            return Response({'detail': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)    

class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        user=request.user
        if user.is_anonymous:
            return Response({"detail": "User must be authenticated to change the password."},status=status.HTTP_401_UNAUTHORIZED)
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            password=serializer.validated_data['password']
            confirm_password=serializer.validated_data['confirm_password']
            if password!=confirm_password:
                return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                password_validation.validate_password(password,user)
            except DjangoValidationError as e:
                return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(password)
            print(user,"========12")
            user.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

