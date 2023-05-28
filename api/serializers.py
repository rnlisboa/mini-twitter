from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ProfileUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileUserModel
        fields = '__all__'

class UserPostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserPostModel
        fields = '__all__'