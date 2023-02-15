from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import utils.file as fileutils
from .models import UserAccount


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            if not user.is_blocked:
                return user
            raise serializers.ValidationError("서비스 이용이 정지된 계정입니다.")
        raise serializers.ValidationError("비밀번호가 틀렸거나 존재하지 않는 계정입니다.")

    def create(self, _validated_data):
        pass

    def update(self, _instance, _validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('username', 'visiblename', 'permission', 'studentid', 'profileimage')


class DetailedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('username', 'visiblename', 'email', 'permission', 'studentid', 'profileimage')


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    visiblename = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_chk = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    profileimage = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserAccount
        fields = ('username', 'visiblename', 'password', 'password_chk', 'email', 'profileimage')
        extra_kwargs = {
            'password': {'write_only': True},
            'password_chk': {'write_only': True},
        }

    def validate(self, attrs):
        errors = []
        username = attrs['username']
        visiblename = attrs['visiblename']
        password = attrs['password']
        password_chk = attrs['password_chk']
        email = attrs['email']

        if password != password_chk:
            errors.append('비밀번호가 일치하지 않습니다.')

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
            errors.append('아이디는 5자 이상이어야 합니다.')

        if len(visiblename) < 3:
            errors.append('이름은 3자 이상이어야 합니다.')

        if len(password) < 8:
            errors.append('비밀번호는 8자 이상이어야 합니다.')

        if UserAccount.objects.filter(username=username).exists():
            errors.append('이미 존재하는 아이디입니다.')

        if UserAccount.objects.filter(email=email).exists():
            errors.append('이미 존재하는 이메일입니다.')

        if UserAccount.objects.filter(visiblename=visiblename).exists():
            errors.append('이미 존재하는 이름입니다.')

        if email[email.find('@'):] != '@bjungang.hs.kr':
            errors.append('학교 이메일이 아닙니다.')

        if not email[:email.find('@') - 1].isnumeric():
            errors.append('이메일 사용자명이 학번이 아닙니다. 가입을 원할 경우 관리자에게 문의하세요.')

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
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
