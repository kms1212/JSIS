import enum

from django.core.paginator import Paginator

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from utils.search import advanced_search
from .serializers import NoticeSerializer, NoticeListSerializer
from .models import Notice, Reply

# Create your views here.
class NoticeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()

    class OrderBy(enum.Enum):
        ID = 'noticeid'
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
        # When noticeid is provided, return the article with that id
        noticeid = request.GET.get('noticeid')

        # When noticeid is not provided, return article list
        # Listing parameters:
        #   - page: page number
        #   - count: number of articles per page
        #   - order: order by
        #   - search: search query
        page = request.GET.get('page', '1')
        count = request.GET.get('count', '10')
        order = request.GET.get('order')
        search = request.GET.get('search')

        if noticeid:
            # Return article
            try:
                article = Notice.objects.get(noticeid=noticeid, deleted=False)
            except Notice.DoesNotExist:
                return Response(
                    {
                        "message": "Article not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            article.views += 1
            article.save()
            serializer = NoticeSerializer(article)
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

        articles = Notice.objects.filter(deleted=False).order_by(orderdirection.value +
                                                                  orderby.value)

        if search:
            articles = advanced_search(articles, search)

        paginator = Paginator(articles, count)
        articles = paginator.get_page(page)
        serializer = NoticeListSerializer(articles, many=True)

        return Response({
            "page": int(page),
            "pages": paginator.num_pages,
            "count": count,
            "total": paginator.count,
            "list": serializer.data
        })

