from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_admin', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_active', 'is_admin', 'created_at', 'updated_at']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ['user', 'access_token', 'refresh_token']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']