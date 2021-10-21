from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    phone = serializers.CharField(required=True, max_length=15)
    photo = serializers.FileField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.phone = validated_data.get('title', instance.title)
        instance.photo = validated_data.get('code', instance.code)
        instance.save()
        return instance