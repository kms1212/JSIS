from django.db import models
from authapi.models import UserAccount, File


class Reply(models.Model):
    replyid = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserAccount,
                               on_delete=models.CASCADE, null=True,
                               related_name='community_%(class)s_author')
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.BooleanField(default=False)
    text = models.TextField()
    replies = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return '@' + self.author.username + ': ' + self.text[:20]


class ArticleTypes(models.IntegerChoices):
    INSTA = 0, '사진'
    DOCUMENT = 1, '문서'


class Article(models.Model):
    articleid = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserAccount,
                               on_delete=models.CASCADE,
                               related_name='community_%(class)s_author',
                               null=True)
    title = models.CharField(max_length=255, null=True)
    type = models.IntegerField(default=ArticleTypes.INSTA,choices=ArticleTypes.choices)
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
