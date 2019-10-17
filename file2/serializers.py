from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Document, CustomUser


class DocumentSerializer(serializers.ModelSerializer):

    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Document
        fields = '__all__'



    # def update(self, instance, validated_data):
    #     instance.docfile = validated_data.get('docfile', instance.docfile)
    #
    #     instance.save()
    #     return instance

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
