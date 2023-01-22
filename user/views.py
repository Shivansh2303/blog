from .models import UserModel
from .utils import send_verification
from .serializers import UserRegisterSerializer,LoginSerializer

from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site

import jwt

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken



class UserCreateAPIView(generics.CreateAPIView):
    serializer_class=UserRegisterSerializer
    permission_classes=(AllowAny,)
    
    def post(self, request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user=UserModel.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token
        current_site=get_current_site(request).domain
        reverse_link=reverse('verify-email')

        absurl="http://"+current_site+reverse_link+"?token="+ str(token)
        body="Hi,"+user_data['username'] +"\n To verify your email click on the link below \n"+ absurl


        data={
            'subject':"verification mail",
            'body':body,
            'to_email':user_data['email'],
            'from_email':"shivanshkate@mail.com",

        }
        send_verification(data)
        status_code=status.HTTP_201_CREATED
        response={
            'success':'True',
            'status code':status_code,
            'message':"User registered successfully and a link has been to the registered email address for verification"
        }
        return Response(response,status=status_code)
            
class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256',])
            user=UserModel.objects.get(id=payload['user_id'])
            user.is_active=True
            # print(payload)
            
            return Response({"email":"Successfully verified and you account is activated"})
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error":"Activation link expired "})
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error":"Invalid token "})
        

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response={
            'success':'True',
            'status code':status.HTTP_200_OK,
            'message':'User has been logged in successfully',
            'token':'token'
        }
        status_code=status.HTTP_200_OK        
        
        return Response(response,status_code)




        

        



class UserDetailDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=UserModel.objects.all()
    serializer_class=UserRegisterSerializer
    lookup_field='pk'




    



