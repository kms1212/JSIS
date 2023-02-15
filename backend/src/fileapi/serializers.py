from rest_framework import serializers
import utils.file as fileutils
from .models import File


class FileInfoSerializer(serializers.ModelSerializer):
    data_size = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('mimetype', 'filename', 'data_size', 'date_uploaded', 'uploader', 'fileid')

    def get_data_size(self, obj):
        return fileutils.get_size_from_file(obj)
