from django.db import models
from authapi.models import UserAccount, File
from bbsbaseapi.models import Reply

# Create your models here.
class Notice(models.Model):
    noticeid = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserAccount,
                               on_delete=models.CASCADE,
                               related_name='mainbbs_%(class)s_author',
                               null=True)
    title = models.CharField(max_length=255, null=True)
    document = models.TextField()
    views = models.IntegerField(default=0)
    files = models.ManyToManyField(File,
                                   blank=True,
                                   related_name='mainbbs_%(class)s_files')
    likes = models.ManyToManyField(UserAccount,
                                   blank=True,
                                   related_name='mainbbs_%(class)s_likes')
    replies = models.ManyToManyField(Reply,
                                     blank=True,
                                     related_name='mainbbs_%(class)s_replies')
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '@' + self.author.username + ': ' + self.title[:20]


class CardNotice(models.Model):
    cnid = models.AutoField(primary_key=True)
    image = models.ForeignKey(File,
                              on_delete=models.CASCADE,
                              related_name='mainbbs_%(class)s_image', null=True)
    alt = models.TextField()
    priority = models.IntegerField()
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True)
    until = models.DateTimeField()

    def __str__(self):
        return self.alt[:20]
