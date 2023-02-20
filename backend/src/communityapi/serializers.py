from rest_framework import serializers

from authapi.serializers import UserSerializer

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('postid',
                  'title',
                  'document',
                  'author',
                  'created',
                  'modified',
                  'views',
                  'files',
                  'likes_count',
                  'replies_count',
                  'type')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('postid',
                  'title',
                  'author',
                  'created',
                  'views',
                  'likes_count',
                  'replies_count',
                  'type')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()
