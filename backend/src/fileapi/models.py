from django.db import models


class File(models.Model):
    class AccessScope(models.IntegerChoices):
        PRIVATE = 0, 'private'
        RESTRICTED = 1, 'restricted'
        PUBLIC = 2, 'public'
        ANYONE = 3, 'anyone'

    fileid = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)
    data = models.FileField(upload_to='file')
    uploader = models.ForeignKey('authapi.UserAccount', on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    access_scope = models.IntegerField(default=AccessScope.PUBLIC, choices=AccessScope.choices)
    attribute = models.JSONField(default=dict)

    def __str__(self):
        return '@' + self.uploader.username + ': ' + self.data.name
