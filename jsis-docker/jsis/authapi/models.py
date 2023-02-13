from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from fileapi.models import File

class UserPermissions(models.IntegerChoices):
    USER = 0
    HQ = 1
    TEACHER = 2
    OTHER = 3


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, visiblename, studentid, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not visiblename:
            raise ValueError('Users must have a visible name')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            visiblename=visiblename,
            studentid=studentid,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, visiblename, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            visiblename=visiblename,
            studentid='',
            password=password,
        )

        user.is_staff = True
        user.is_active = True
        user.permission = UserPermissions.OTHER

        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    visiblename = models.CharField(max_length=40, unique=True)
    profileimage = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True, related_name='profileimage')
    email = models.EmailField(max_length=255, unique=True)
    studentid = models.CharField(max_length=4, unique=True, blank=True, null=True)
    permission = models.IntegerField(default=UserPermissions.USER, choices=UserPermissions.choices)
    agreement_status = models.JSONField(blank=True, null=True, default=dict)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_lastlogin = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_blocked_anon = models.BooleanField(default=False)
    block_reason = models.TextField(default="", blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'visiblename']

    objects = UserAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True
