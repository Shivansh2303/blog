from .models import UserModel
from .utils import send_verification
from .serializers import *
from article.models import Article
from mindRetreats.permissions import IsOwnerOrReadOnly


from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
# from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

import jwt

from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions 




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
        body="Hi,"+user_data['user_name'] +"\n To verify your email click on the link below \n"+ absurl


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
            user.is_staff=True
            user.save()
            # print("file=" ,__file__,"user=",user.is_active)
            
            return Response({"email":"Successfully verified and you account is activated"})
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error":"Activation link expired "})
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error":"Invalid token "})
        

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer    
    
    def post(self,request,*args,**kwargs):
        try:
            serializer=self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.validated_data
            login(request,user)
            response={
                'user':user.user_name,
                'status code':status.HTTP_200_OK,
                'success message':'User has been logged in successfully',
                
            }
            status_code=status.HTTP_200_OK        
            
            return Response(response,status_code)
        
        except serializers.ValidationError:
            return Response(
                data=serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        except Exception as e:
            return Response(
                data={"error":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class RequestPasswordResetEmail(generics.GenericAPIView):
    queryset=UserModel.objects.all()
    serializer_class=RequestResetPassword

    def post(self, request):
        email=request.data['email']
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if UserModel.objects.filter(email=email).exists():
            user=UserModel.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            reverse_link=reverse('password-reset',kwargs={'uidb64':uidb64,'token':token})
            current_site=get_current_site(request).domain
            abs_url="http://"+current_site+reverse_link
            body=user.user_name+"\n We'd been told that you'd like to change the password for your account. \n If you made such request, set a new passord by clicking the link below \n"+abs_url+"\n if it  wasn't you, simply ignore this email and your pasword will remain the same. "

            data={
                'subject':"Reset Password",
                'body':body,
                'from_email':"shivanshkate@gmail.com",
                'to_email':user.user_name
            }

            send_verification(data)

            return Response(serializer.data,status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request,uidb64,token):
        try:
           id =smart_str(urlsafe_base64_decode(uidb64))
           user=UserModel.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'token is not valid, please check the new one'},status=status.HTTP_401_UNAUTHORIZED)
           return Response({
                'success':True,
                'message':'Credential valid','uidb64':uidb64,'token':token,
            },
            status=status.HTTP_200_OK
            )
        except DjangoUnicodeDecodeError as indentifier:
            return Response({
                'error':'token is not valid, please check the new one'
            },
            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    queryset=UserModel.objects.all()
    serializer_class=ResetPasswordSerializer

    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_100_CONTINUE)
        
        

        
class UserDetailDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset=UserModel.objects.all()
    serializer_class=UserProfileSerializer
    lookup_field='pk'

    # def get(self, request,pk,*args,**kwargs):
        
        # print(serializer.data)
        # try:
        #     serializer=self.serializer_class(instance=request.user.id)
        #     # user_profile=UserModel.objects.get(id=pk)
        #     user_profile=serializer.data
        #     status_code=status.HTTP_200_OK
            
        #     response={
        #         'success':True,
        #         'status_code':status_code,
        #         'message':'User Profile  fetch successfully',
        #         # 'data':
        #         #     {
        #         #     'user_name':user_profile.user_name,
        #         #     'email':user_profile.email,
        #         #     'active':user_profile.is_active,
        #         #     'staff':user_profile.is_staff,
        #         #     'posts':user_profile
                    
                    
        #         #     }
        #     }
        # except Exception as e:
        #     status_code=status.HTTP_400_BAD_REQUEST
        #     response={
        #         'success':False,
        #         'status_code':status_code,
        #         'message':'User does not exists',
        #     }
        
    def retrieve(self, request,pk=None):
        queryset=UserModel.objects.get(pk=pk)
        
        serializer=UserProfileSerializer(queryset,context={'request':request})
        # serializer=UserProfileSerializer(queryset)
        
        
        return Response(serializer.data)



    



