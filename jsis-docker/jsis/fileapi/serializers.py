from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import utils.file as fileutils
from .models import File


class FileSerializer(serializers.ModelSerializer):
    data_base64 = serializers.SerializerMethodField()
    data_size = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('data_base64', 'mimetype', 'filename', 'data_size', 'date_uploaded', 'uploader', 'fileid')

    def get_data_base64(self, obj):
        return fileutils.get_base64_from_file(obj)

    def get_data_size(self, obj):
        return fileutils.get_size_from_file(obj)


class FileInfoSerializer(serializers.ModelSerializer):
    data_size = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('mimetype', 'filename', 'data_size', 'date_uploaded', 'uploader', 'fileid')

    def get_data_size(self, obj):
        return fileutils.get_size_from_file(obj)

