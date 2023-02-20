'''
Models configuration for the authapi.

Defined models
--------------
* UserAccount - User account model
    * UserAccountManager - User account manager
    * UserPermissions - User permission levels

Revision History
----------------
* 2020-02-??: Created by @kms1212.
* 2020-02-18: Documented by @kms1212.
'''

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from fileapi.models import File

class UserPermissions(models.IntegerChoices):
    """
    User permission levels

    Choices
    -------
    :USER:    Student user
    :HQ:      Student headquarter user
    :TEACHER: Teacher user
    :OTHER:   Other user

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """
    USER = 0
    HQ = 1
    TEACHER = 2
    OTHER = 3


class UserAccountManager(BaseUserManager):
    """
    User account manager
    Creates user or superuser
    """

    def create_user(self, username, email, visiblename, studentid, password=None):  # pylint: disable=too-many-arguments
        """
        Create user

        Parameters / Return Values
        --------------------------

        :param username: User name (for login)
        :param email: User email
        :param visiblename: User nickname
        :param studentid: Student ID (Format: GCXX, G: Grade, C: Class, XX: Class ID)
        :param password: Account password
        :returns: UserAccount object

        Revision History
        ----------------
        * 2020-02-??: Created by @kms1212.
        * 2020-02-18: Documented by @kms1212.
        """

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
        """
        Create superuser

        Parameters / Return Values
        --------------------------

        :param username: User name (for login)
        :param email: User email
        :param visiblename: User nickname
        :param password: Account password
        :returns: UserAccount object

        Revision History
        ----------------
        * 2020-02-??: Created by @kms1212.
        * 2020-02-18: Documented by @kms1212.
        """
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
    """
    User account model

    Attributes
    ----------
    :userid:           Auto-generated id for primary key
    :username:         User name (for login)
    :visiblename:      User nickname
    :profileimage:     Profile image (File model FK)
    :email:            User email (Basic format: YYGCXX@bjungang.hs.kr, other email if not student)
    :studentid:        Student ID (Format: GCXX, G: Grade, C: Class, XX: Class ID)
    :permission:       Choice (UserPermissions)
    :description:      User description
    :agreement_status: User agreement status: JSON
    :date_joined:      Initialized when user created
    :date_lastlogin:   Updated when user logged in
    :is_blocked:       True if user blocked
    :is_blocked_anon:  True if user blocked to anonymous activity
    :block_reason:     Block reason
    :is_staff:         True if user is superuser
    :is_active:        True if user is active

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    visiblename = models.CharField(max_length=40, unique=True)
    profileimage = models.ForeignKey(File,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='profileimage')
    email = models.EmailField(max_length=255, unique=True)
    studentid = models.CharField(max_length=4, unique=True, blank=True, null=True)
    permission = models.IntegerField(default=UserPermissions.USER, choices=UserPermissions.choices)
    description = models.TextField(default="", blank=True)
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
        """
        Model stringify
        """
        return f'{self.studentid} {self.visiblename} @{self.username}'

    def has_perm(self, _perm, _obj=None):
        """
        Check if user has permission
        """
        return self.is_staff

    def has_module_perms(self, _app_label):
        """
        Check if user has permission
        """
        return True
