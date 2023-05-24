from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ProfileUserModel
        fields = '__all__'

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.UserPostModel
        fields = '__all__'