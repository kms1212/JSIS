from rest_framework import serializers
from .models import UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Article, Reply, CardNotice, File
from authapi.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title', 'document', 'author', 'created', 'modified', 'views', 'files', 'likes_count', 'replies_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('articleid', 'title', 'author', 'created', 'views', 'likes_count', 'replies_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()
