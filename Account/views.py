# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, mixins,permissions,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .permissions import *
from .utils import *
from models import profile
from PIL import Image 
import json
#from .permissions import AnonPermissionOnly
from .serializers import UserRegisterSerializer ,UserProfileSerializer

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


from django.contrib.auth.models import User

# class AuthAPIView(APIView):
#     permission_classes      = [AnonPermissionOnly]
#     def post(self, request, *args, **kwargs):
#         print(request.user)
#         if request.user.is_authenticated():
#             return Response({'detail': 'You are already authenticated'}, status=400)
#         data = request.data
#         username = data.get('username') # username or email address
        
#         password = data.get('password')
#         qs = User.objects.filter(Q(username__iexact=username)|Q(email__iexact=username)).distinct()
        
#         if qs:
#             user_obj = qs.first()
#             if user_obj.check_password(password):
#                 user = user_obj
#                 payload = jwt_payload_handler(user)
#                 token = jwt_encode_handler(payload)
#                 response = jwt_response_payload_handler(token, user, request=request)
#                 return Response(response)

#       return Response({"detail": "Invalid credentials"}, status=401)
# Create your views here.
class RegisterAPIView(generics.CreateAPIView):
    queryset                = User.objects.all()
    serializer_class        = UserRegisterSerializer
    permission_classes      = [AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

#needs JWT Token as header and in body  phone and image(optional)
#will return profile data for a authorised user

class ProfileAPIView(APIView,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    #permission_classes          =[permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class            = UserProfileSerializer
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        user = request.user

        phone = request.data.get('phone')#must be starting with 91 and of 10 digits
        image = request.data.get('image')

        
        profile.phone = phone
        profile.image = image

        profile.save()

        data = UserProfileSerializer(profile).data

        return Response({'body':data}, status=HTTP_200_OK)


class UpdateProfile(APIView):
    permission_classes          =[permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class        =UserProfileSerializer
    def post(self, request, *args, **kwargs):
        user = request.user
        
           
        try:
            flag=True
            files=request.FILES.get('Image')
            
        except expression as identifier:
            flag=False
        
            
        phone = request.data.get('phone')
        profile_obj = profile.objects.get(user=user)
        profile_obj.phone = phone
        if flag:
            profile_obj.image = files
        profile_obj.save()
        
        data = UserProfileSerializer(profile_obj).data

        return Response({"body":data}, status=200)
#return JWT KEY if the user is authenticated 
#needs username or email and password from body
class Login(APIView):

    permission_classes      = [AnonPermissionOnly]
    def post(self, request, *args, **kwargs):
        #print(request.user)
        if request.user.is_authenticated():
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        username =data.get('username') # username or email address
        password =data.get('password')  #password
        qs = User.objects.filter(
                Q(username__iexact=username)|
                Q(email__iexact=username)
            ).distinct()
        
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
            

        return Response({"detail": "Invalid credentials"}, status=401)
    
