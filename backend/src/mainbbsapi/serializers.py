from rest_framework import serializers

from authapi.serializers import UserSerializer
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title',
                  'document',
                  'author',
                  'created',
                  'modified',
                  'views',
                  'files',
                  'likes_count',
                  'replies_count')

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
        fields = ('articleid',
                  'title',
                  'author',
                  'created',
                  'views',
                  'likes_count',
                  'replies_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()
