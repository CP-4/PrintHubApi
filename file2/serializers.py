from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Document

# in models.py

# class Comment(object):
#     def __init__(self, email, content, created=None):
#         self.email = email
#         self.content = content
#         self.created = created or datetime.now()
#
# comment = Comment(email='leila@example.com', content='foo bar')

# in serializers.py

# class CommentSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()

# class SongsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Songs
#         fields = ("title", "artist")
#
#     def update(self, instance, validated_data):
#             instance.title = validated_data.get("title", instance.title)
#             instance.artist = validated_data.get("artist", instance.artist)
#             instance.save()
#             return instance

# models.py

# class Document(models.Model):
#     docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        # fields = {'docfile'}
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
