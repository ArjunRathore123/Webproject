from rest_framework import serializers
from accounts.models import CustomUser


class BuyerRegisterSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['id','email','password','confirm_password','first_name','last_name','contact','gender','date_of_birth','address','user_type']

    def validate(self,data):
        user_type=data.get('user_type',None)
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError('Password does not match')
        if user_type and user_type.lower()=='seller':
            raise serializers.ValidationError("seller registration not allowed")
        return data 

    def create(self,validate_data):
        validate_data.pop('confirm_password',None)
       
        return CustomUser.objects.create_user(**validate_data)
    
class BuyerLoginSerialzier(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    

class ForgetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)