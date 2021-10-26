from rest_framework import serializers
from .models import User, SelfReview


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'sbis', 'password')


class SelfReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfReview
        fields = '__all__'
