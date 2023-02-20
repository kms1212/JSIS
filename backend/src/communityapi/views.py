import enum

from django.core.paginator import Paginator

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from utils.search import advanced_search
from .serializers import PostSerializer, PostListSerializer
from .models import Post

# Create your views here.
class PostAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    class OrderBy(enum.Enum):
        ID = 'postid'
        TITLE = 'title'
        CREATED = 'created'

    class OrderDirection(enum.Enum):
        ASC = ''
        DESC = '-'

    def parse_order_parameter(self, order):
        if order is not None:
            if order.find('-') != -1:
                (orderby, orderdirection) = order[:order.find('-')], order[order.find('-') + 1:]

                orderby = self.OrderBy[orderby.upper()]
                orderdirection = self.OrderDirection[orderdirection.upper()]
            else:
                orderby = self.OrderBy[order.upper()]

                if orderby == self.OrderBy.TITLE:
                    orderdirection = self.OrderDirection.ASC
                else:
                    orderdirection = self.OrderDirection.DESC
        else:
            (orderby, orderdirection) = (self.OrderBy.CREATED, self.OrderDirection.DESC)

        return (orderby, orderdirection)


    def get(self, request):
        # When postid is provided, return the article with that id
        postid = request.GET.get('postid')

        # When postid is not provided, return article list
        # Listing parameters:
        #   - page: page number
        #   - count: number of articles per page
        #   - order: order by
        #   - search: search query
        page = request.GET.get('page', '1')
        count = request.GET.get('count', '10')
        order = request.GET.get('order')
        search = request.GET.get('search')

        if postid:
            # Return article
            try:
                article = Post.objects.get(postid=postid, deleted=False)
            except Post.DoesNotExist:
                return Response(
                    {
                        "message": "Post not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            article.views += 1
            article.save()
            serializer = PostSerializer(article)
            return Response(serializer.data)

        # Return article list
        try:
            (orderby, orderdirection) = self.parse_order_parameter(order)
        except KeyError:
            return Response(
                {
                    "message": "Invalid order parameter"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        articles = Post.objects.filter(deleted=False).order_by(orderdirection.value +
                                                                  orderby.value)

        if search:
            articles = advanced_search(articles, search)

        paginator = Paginator(articles, count)
        articles = paginator.get_page(page)
        serializer = PostListSerializer(articles, many=True)

        return Response({
            "page": int(page),
            "pages": paginator.num_pages,
            "count": count,
            "total": paginator.count,
            "list": serializer.data
        })
