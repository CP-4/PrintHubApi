from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Document, CustomUser, UrlAnalytics, GuestStudent, Shop


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


class GuestStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestStudent
        fields = '__all__'


class UrlAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlAnalytics
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Shop
        fields = '__all__'
