from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileUserModel
        fields = '__all__'

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostModel
        fields = '__all__'