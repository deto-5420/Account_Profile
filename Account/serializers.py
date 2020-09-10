import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import profile
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta             = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()
class UserRegisterSerializer(serializers.ModelSerializer):
    password2           = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token               = serializers.SerializerMethodField(read_only=True)
    expires             = serializers.SerializerMethodField(read_only=True)
    message             = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',

            'message',

        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering. Please verify your email before continuing."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists")
        return value

    def get_token(self, obj): 
         user = obj
         payload = jwt_payload_handler(user)
         token = jwt_encode_handler(payload)
         return token

    def validate(self, data):
        pw  = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):  
        #print(validated_data)
        user_obj = User(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),  
                username=validated_data.get('username'), 
                email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = True
        user_obj.save()
        return user_obj    
   


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name',
            'last_name',
            'username',
            'email'
        ]
 
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = profile
        fields=[
            'user',
            'image',
            'phone'
        ]
    
    def get_user(self, obj):
        return UserDetailSerializer(obj.user).data

# class LoginSerializer(serializers.Serializer):
#     user_name=serializers.SerializerMethodField()
#     password=serializers.SerializerMethodField(style={'input_type': 'password'} )
#     def create(self, validated_data):  
#         data = {
#                 username :  validated_data.get('user_name') ,
#                 email : validated_data.get('password')
#         }
        
#         return data 