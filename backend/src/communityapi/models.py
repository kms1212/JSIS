from django.db import models
from authapi.models import UserAccount, File
from bbsbaseapi.models import Reply


class PostTypes(models.IntegerChoices):
    INSTA = 0, '사진'
    DOCUMENT = 1, '문서'


class Post(models.Model):
    postid = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserAccount,
                               on_delete=models.CASCADE,
                               related_name='community_%(class)s_author',
                               null=True)
    title = models.CharField(max_length=255, null=True)
    type = models.IntegerField(default=PostTypes.INSTA, choices=PostTypes.choices)
    document = models.TextField()
    views = models.IntegerField(default=0)
    files = models.ManyToManyField(File,
                                   blank=True,
                                   related_name='community_%(class)s_files')
    likes = models.ManyToManyField(UserAccount,
                                   blank=True,
                                   related_name='community_%(class)s_likes')
    replies = models.ManyToManyField(Reply,
                                     blank=True,
                                     related_name='community_%(class)s_replies')
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '@' + self.author.username + ': ' + self.title[:20]
