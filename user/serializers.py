from .models import UserModel
from article.serializers import ArticleSerializer


from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.models import update_last_login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError


from rest_framework import status
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings 
from rest_framework.validators import UniqueValidator


JWT_PAYLOAD_HANDLER=api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER=api_settings.JWT_ENCODE_HANDLER

class UserRegisterSerializer(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=UserModel
        fields=['id','email','user_name','password']
        
    def create(self, validated_data):
        user=super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.CharField(required=True)
    password=serializers.CharField(required=True,write_only=True)
    class Meta:
        model=UserModel
        fields=['email','password']

    def validate(self,data):
        # print(data)
        email=data.get('email',None)
        password=data.get('password',None)
        
        user=authenticate(email=email,password=password)

        if user is None:
            raise serializers.ValidationError('Invalid Credentials')

        try:
            payload=JWT_PAYLOAD_HANDLER(user)
            jwt_token=JWT_ENCODE_HANDLER(payload)
            update_last_login(None,user)
            # print("qwertty====",user)
            return user
        except User.DoesNotExist:
            raise serializers.ValidateError("User with given email and password does not exists. ")
        
        return super().validate(data)


class RequestResetPassword(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=UserModel
        fields=['email']
class ResetPasswordSerializer(serializers.ModelSerializer):
    
    password=serializers.CharField(min_length=8,max_length=60,write_only=True)
    token=serializers.CharField(min_length=1,write_only=True)
    uidb64=serializers.CharField(min_length=1,write_only=True)
    class Meta:
        model=UserModel
        fields=['password','token','uidb64']
    
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            
            id=force_str(urlsafe_base64_decode(uidb64))
            user=UserModel.objects.get(id=id)
            if not PasswordResetTokenGenrator().check_token(user,token):
                user.set_password(password)
                user.save()
                return user
        except:
            raise  serializers.ValidationError('Token Expires')
        return super().validate(attrs)

class UserProfileSerializer(serializers.ModelSerializer):
    # posts=serializers.PrimaryKeyRelatedField(read_only=True)
    
    posts=serializers.HyperlinkedIdentityField('article-detail',lookup_field='pk')
    class Meta:
        model=UserModel
        fields=['id','email','posts' ]
 