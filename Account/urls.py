from django.conf.urls import url, include
from django.contrib import admin


from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token # accounts app

from .views import RegisterAPIView,ProfileAPIView,Login,UpdateProfile
urlpatterns = [
   # url(r'^$', AuthAPIView.as_view(), name='login'),
    url(r'^jwt/$', obtain_jwt_token),
    url(r'^jwt/refresh/$', refresh_jwt_token),
    url(r'^register/$', RegisterAPIView.as_view(), name='register'), 
    url(r'^profile/$', UpdateProfile.as_view(), name='profile'),
    url(r'^login/$',Login.as_view(),name='login')
]