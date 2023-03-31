from rest_framework import serializers
from .models import *

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'friends', 'requests']

class ChatroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'profile']

class PictureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image', 'profile']

class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'message', 'profile', 'datetime']
