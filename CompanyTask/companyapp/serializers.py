
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()
    # estimation_files = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
    

    class Meta:
        model = User
        fields = ('id','email','password','tokens')

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.get(email=email)
        
        user = filtered_user_by_email.check_password(password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not filtered_user_by_email.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        token, _ = Token.objects.get_or_create(user=user)
  
        return {
            'id':filtered_user_by_email.id,
            'email': filtered_user_by_email.email,
            'tokens': filtered_user_by_email.tokens,
        }
        