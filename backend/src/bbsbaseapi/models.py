from django.db import models
from authapi.models import UserAccount

# Create your models here.
class Reply(models.Model):
    replyid = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserAccount,
                               on_delete=models.CASCADE,
                               null=True,
                               related_name='mainbbs_%(class)s_author')
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.BooleanField(default=False)
    text = models.TextField()
    replies = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return '@' + self.author.username + ': ' + self.text[:20]
