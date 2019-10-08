from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.docfile = validated_data.get('docfile', instance.docfile)

        instance.save()
        return instance

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
