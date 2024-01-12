from rest_framework import generics
from .serilaizers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from accounts.models import CustomUser

class UserView(ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=UserSerializer