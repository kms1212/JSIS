from rest_framework import serializers

from authapi.serializers import UserSerializer
from .models import Reply

class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    def get_replies(self, obj):
        current_depth = self.context.get('depth', 0)

        if current_depth > 0:
            replies = obj.replies.all()
            print(obj.replyid, len(replies), current_depth, flush=True)
            return ReplySerializer(replies, many=True, context={ 'depth': current_depth - 1 }).data
        return []

    def get_reply_count(self, obj):
        return obj.replies.count()

    class Meta:
        model = Reply
        fields = ('replyid',
                  'author',
                  'created',
                  'modified',
                  'text',
                  'replies',
                  'reply_count')