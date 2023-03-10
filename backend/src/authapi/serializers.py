# pylint: disable=line-too-long
"""
Serializers configuration for the authapi.

Serializers
-----------
:class:`LoginSerializer` - username, password serializer for LoginView
:class:`UserSerializer` - Simplified serializer for user basic information. (No personal information included)
:class:`DetailedUserSerializer` - Detailed serial for user basic information. (Personal information included)
:class:`RegisterSerializer` - User basic information input serializer for user registration

Revision History
----------------
* 2020-02-??: Created by @kms1212.
* 2020-02-18: Documented by @kms1212.
"""
# pylint: enable=line-too-long

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import serializers

import utils.file as fileutils
from communityapi.models import Post, Reply
from .models import UserAccount


class LoginSerializer(serializers.Serializer):
    """
    Login Serializer

    Fields
    ------
    :attrib username: Username
    :attrib password: RAW Password

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        User login validator

        Description
        -----------
        Check username and password
        Block login if user attribute "is_blocked" is True

        Parameters / Return Values
        --------------------------
        :param attrs: Serializer attribute
        :returns: authapi.models.UserAccount if valid user, None if not (raises Error)

        Possible Errors
        ---------------
        :serializers.ValidationError:
            Raised with error message when invalid user is trying to login

        Revision History
        ----------------
        * 2020-02-??: Created by @kms1212.
        * 2020-02-18: Documented by @kms1212.
        """
        user = authenticate(**attrs)
        if user and user.is_active:
            if not user.is_blocked:
                return user
            raise serializers.ValidationError("????????? ????????? ????????? ???????????????.")
        raise serializers.ValidationError("??????????????? ???????????? ???????????? ?????? ???????????????.")


class UserSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user basic information. (No personal information included)

    Fields
    ------
    :attrib userid:       User ID
    :attrib username:     Username
    :attrib visiblename:  User nickname
    :attrib permission:   User permission level
    :attrib studentid:    Student ID
    :attrib profileimage: Profile image
    :attrib description:  User description
    :attrib post_count:   User post count
    :attrib reply_count:  User reply count

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """

    post_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        """
        Internal method for getting user post count
        """
        return Post.objects.filter(author=obj).count()

    def get_reply_count(self, obj):
        """
        Internal method for getting user reply count
        """
        return Reply.objects.filter(author=obj).count()

    class Meta:  # pylint: disable=missing-class-docstring
        model = UserAccount
        fields = (
            'userid',
            'username',
            'visiblename',
            'permission',
            'studentid',
            'profileimage',
            'description',
            'post_count',
            'reply_count',
            )


class DetailedUserSerializer(serializers.ModelSerializer):
    """
    Detailed serial for user basic information. (Personal information included)

    Fields
    ------
    :attrib userid:           User ID
    :attrib username:         Username
    :attrib visiblename:      User nickname
    :attrib email:            User email
    :attrib permission:       User permission level
    :attrib studentid:        Student ID
    :attrib profileimage:     Profile image
    :attrib description:      User description
    :attrib date_joined:      User registration date
    :attrib date_lastlogin:   User last login date
    :attrib is_blocked:       User block status
    :attrib is_blocked_anon:  User anonymous block status
    :attrib block_reason:     User block reason
    :attrib agreement_status: User agreement status
    :attrib post_count:       User post count
    :attrib reply_count:      User reply count

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """

    post_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        """
        Internal method for getting user post count
        """
        return Post.objects.filter(author=obj).count()

    def get_reply_count(self, obj):
        """
        Internal method for getting user reply count
        """
        return Reply.objects.filter(author=obj).count()

    class Meta:  # pylint: disable=missing-class-docstring
        model = UserAccount
        fields = (
            'userid',
            'username',
            'visiblename',
            'email',
            'permission',
            'studentid',
            'profileimage',
            'description',
            'date_joined',
            'date_lastlogin',
            'is_blocked',
            'is_blocked_anon',
            'block_reason',
            'agreement_status',
            'post_count',
            'reply_count',
            )


class RegisterSerializer(serializers.ModelSerializer):
    """
    User basic information input serializer for user registration

    Fields
    ------
    :attrib username:           Username
    :attrib visiblename:        User nickname
    :attrib password:           Password
    :attrib password_chk:       Repeated password (TODO: delete it)
    :attrib email:              User email
    :attrib profileimage:       User profile image

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """

    username = serializers.CharField(required=True)
    visiblename = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_chk = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    profileimage = serializers.ImageField(required=False, allow_null=True)

    class Meta:  # pylint: disable=missing-class-docstring
        model = UserAccount
        fields = ('username', 'visiblename', 'password', 'password_chk', 'email', 'profileimage')
        extra_kwargs = {
            'password': {'write_only': True},
            'password_chk': {'write_only': True},
        }

    def validate(self, attrs):
        """
        User registration form validator

        Description
        -----------
        Check username, password, email, visiblename, profileimage
        Check if user already exists
        Raise error if any of the above is not valid

        Parameters / Return Values
        --------------------------
        :param attrs: Serializer attribute
        :returns: attrs if valid, None if not (raises Error)

        Revision History
        ----------------
        * 2020-02-??: Created by @kms1212.
        * 2020-02-18: Documented by @kms1212.
        """
        errors = []
        username = attrs['username']
        visiblename = attrs['visiblename']
        password = attrs['password']
        password_chk = attrs['password_chk']
        email = attrs['email']

        if password != password_chk:
            errors.append('??????????????? ???????????? ????????????.')

        try:
            validate_password(password)
        except ValidationError as error:
            errors.extend(error.messages)

        # validate email
        try:
            validate_email(email)
        except ValidationError as error:
            errors.extend(error.messages)

        if len(username) < 5:
            errors.append('???????????? 5??? ??????????????? ?????????.')

        if len(visiblename) < 3:
            errors.append('????????? 3??? ??????????????? ?????????.')

        if len(password) < 8:
            errors.append('??????????????? 8??? ??????????????? ?????????.')

        if UserAccount.objects.filter(username=username).exists():
            errors.append('?????? ???????????? ??????????????????.')

        if UserAccount.objects.filter(email=email).exists():
            errors.append('?????? ???????????? ??????????????????.')

        if UserAccount.objects.filter(visiblename=visiblename).exists():
            errors.append('?????? ???????????? ???????????????.')

        if email[email.find('@'):] != '@bjungang.hs.kr':
            errors.append('?????? ???????????? ????????????.')

        if not email[:email.find('@') - 1].isnumeric():
            errors.append('????????? ??????????????? ????????? ????????????. ????????? ?????? ?????? ??????????????? ???????????????.')

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        """
        Register user with given validated attributes

        Parameters / Return Values
        --------------------------
        :param validated_data: Validated serializer attribute
        :returns: authapi.models.UserAccount

        Revision History
        ----------------
        * 2020-02-??: Created by @kms1212.
        * 2020-02-18: Documented by @kms1212.
        """
        username = validated_data['username']
        visiblename = validated_data['visiblename']
        password = validated_data['password']
        email = validated_data['email']
        profileimage = validated_data.get('profileimage', None)
        studentid = email[2:email.find('@')]

        user = UserAccount.objects.create_user(username=username,
                                               visiblename=visiblename,
                                               password=password,
                                               email=email,
                                               studentid=studentid)

        if profileimage is not None:
            user.profileimage = fileutils.register_file('ProfileImage', profileimage, user)
            user.save()

        return user
