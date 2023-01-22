from .models import UserModel

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings 
from rest_framework.validators import UniqueValidator

JWT_PAYLOAD_HANDLER=api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLERR=api_settings.JWT_ENCODE_HANDLER

class UserRegisterSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=True,validators=[UniqueValidator(queryset=UserModel.objects.all())])
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=UserModel.objects.all())])
    profile_image=serializers.ImageField(allow_null=True)
    password=serializers.CharField(required=True)
    is_active=serializers.BooleanField(read_only=True)
    # date_joined=serializers.DateTimeField(read_only=True)

    class Meta:
        model=UserModel
        fields='__all__'


class LoginSerializer(serializers.Serializer):
    email=serializers.CharField(required=True)
    password=serializers.CharField(required=True,write_only=True)


    # class Meta:
    #     model=UserModel
    #     fields=['email','password']

    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        print(email,password)
        user= authenticate(email=email,password=password)
        print(user)

        if user is None:
            raise serializers.ValidationError('Invalid credentials.')
        try:
            payload=JWT_PAYLOAD_HANDLER(user)
            jwt_token=JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist():
            raise serializers.ValidationError('User with given email and password does not exists.')
        return {
            'email':user.email,
            'token':jwt_token,
            'message':'You are now logged in ',
        }   

