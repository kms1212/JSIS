from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class File(models.Model):
    fileid = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)
    data = models.FileField(upload_to='file')
    uploader = models.ForeignKey('authapi.UserAccount', on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '@' + self.uploader.username + ': ' + self.data.name

