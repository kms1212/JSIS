from rest_framework import generics, status, permissions
from rest_framework.response import Response

from noticeapi.models import Notice
from communityapi.models import Post
from .serializers import ReplySerializer
from .models import Reply

# Create your views here.
class LikeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def check_parameters(self, request):
        where = request.GET.get('where')
        id = request.GET.get('id')

        if where is None or id is None:
            raise ValueError("Missing parameters")

        if where not in ['notice', 'community_post']:
            raise ValueError("Invalid parameters")

        return (where, id)

    def get_object(self, where, id):
        if where == 'notice':
            return Notice.objects.get(noticeid=id, deleted=False)
        return Post.objects.get(postid=id, deleted=False)

    def get(self, request):
        """
        Get object like status

        URL parameters
        --------------
        :param where: notice or community_post (**required**)
        :param id:    object id (**required**)

        Responses
        ---------
        * 200: Success, returns like status and number of likes
        * 400: Missing parameters (``where``, ``id``)
        * 400: Invalid parameters (``where``: not ``notice`` or ``community_post``)
        * 404: Matching object not found
        """
        try:
            where, id = self.check_parameters(request)
        except ValueError as error:
            return Response({"message": str(error)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            object = self.get_object(where, id)
        except (Notice.DoesNotExist, Post.DoesNotExist):
            return Response({"message": "Matching object not found"},
                            status=status.HTTP_404_NOT_FOUND)

        existance = object.likes.filter(pk=request.user.pk).exists()

        return Response(
            {
                'like': existance,
                'likes': object.likes.count()
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Like an object

        URL parameters
        --------------
        :param where: notice or community_post (**required**)
        :param id:    object id (**required**)

        Responses
        ---------
        * 200: Success, returns like status and number of likes
        * 400: Missing parameters (``where``, ``id``)
        * 404: Matching object not found
        """
        try:
            where, id = self.check_parameters(request)
        except ValueError as error:
            return Response({"message": str(error)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            object = self.get_object(where, id)
        except (Notice.DoesNotExist, Post.DoesNotExist):
            return Response({"message": "Matching object not found"},
                            status=status.HTTP_404_NOT_FOUND)

        existance = object.likes.filter(pk=request.user.pk).exists()
        if existance:
            object.likes.remove(request.user)
        else:
            object.likes.add(request.user)
        object.save()

        return Response(
            {
                'like': not existance,
                'likes': object.likes.count()
            },
            status=status.HTTP_200_OK
        )


class ReplyAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def check_parameters(self, request):
        where = request.GET.get('where')
        id = request.GET.get('id')
        depth = request.GET.get('depth', '0')

        if where is None or id is None:
            raise ValueError("Missing parameters")

        if where not in ['notice', 'community_post', 'reply']:
            raise ValueError("Invalid parameters")

        return (where, id, int(depth))

    def get_object(self, where, id):
        if where == 'notice':
            return Notice.objects.get(noticeid=id, deleted=False)
        elif where == 'community_post':
            return Post.objects.get(postid=id, deleted=False)
        else:
            return Reply.objects.get(replyid=id)

    def get(self, request):
        try:
            where, id, depth = self.check_parameters(request)
        except ValueError as error:
            return Response({"message": str(error)},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            object = self.get_object(where, id)
        except (Notice.DoesNotExist, Post.DoesNotExist, Reply.DoesNotExist):
            return Response({"message": "Matching object not found"},
                            status=status.HTTP_404_NOT_FOUND)
        
        replies = object.replies

        return Response(ReplySerializer(replies, many=True, context={ 'depth': depth }).data, status=status.HTTP_200_OK)
