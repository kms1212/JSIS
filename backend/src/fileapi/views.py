from rest_framework import generics, status, permissions
from rest_framework.response import Response

from django.http.response import HttpResponse

import utils.file as fileutils

from .serializers import FileInfoSerializer
from .models import File


class FileAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = File.objects.all()

    def get(self, request):
        fileid = request.GET.get('fileid')

        if fileid is not None:
            try:
                file = File.objects.get(fileid=fileid)
            except File.DoesNotExist:
                return Response(
                    {
                        "message": "File does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            data = fileutils.get_data_from_file(file)
            response = HttpResponse(data, content_type=file.mimetype)
            response['Content-Disposition'] = 'attachment; filename=' + file.filename

            return response

        return Response(
            {
                "message": "fileid is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class FileInfoAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileInfoSerializer
    queryset = File.objects.all()

    def get(self, request):
        fileid = request.GET.get('fileid')

        if fileid is not None:
            try:
                file = File.objects.get(fileid=fileid)
            except File.DoesNotExist:
                return Response(
                    {
                        "message": "File does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(FileInfoSerializer(file, context=self.get_serializer_context()).data)

        return Response(
            {
                "message": "fileid is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
