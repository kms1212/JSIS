from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
from django.contrib.auth.password_validation import validate_password
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.db.models import Q

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from knox.models import AuthToken

import enum
import datetime

from jsis.settings import SERVER_DOMAIN
from utils.search import advanced_search
from .serializers import ArticleSerializer, ArticleListSerializer
from .models import Article

# Create your views here.
class ArticleAPI(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated ]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    class OrderBy(enum.Enum):
        ID = 'articleid'
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
        # When articleid is provided, return the article with that id
        articleid = request.GET.get('articleid')

        # When articleid is not provided, return article list
        # Listing parameters:
        #   - page: page number
        #   - count: number of articles per page
        #   - order: order by
        #   - search: search query
        page = request.GET.get('page', '1')
        count = request.GET.get('count', '10')
        order = request.GET.get('order')
        search = request.GET.get('search')

        if articleid:
            # Return article
            try:
                article = Article.objects.get(articleid=articleid, deleted=False)
            except Article.DoesNotExist:
                return Response(
                    {
                        "message": "Article not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            article.views += 1
            article.save()
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        else:
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

            articles = Article.objects.filter(deleted=False).order_by(orderdirection.value + orderby.value)

            if search:
                articles = advanced_search(articles, search)

            paginator = Paginator(articles, count)
            articles = paginator.get_page(page)
            serializer = ArticleListSerializer(articles, many=True)

            return Response({
                "page": int(page),
                "pages": paginator.num_pages,
                "count": count,
                "total": paginator.count,
                "articles": serializer.data
            })


class ArticleLikeAPI(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        articleid = request.GET.get('articleid')

        try:
            article = Article.objects.get(articleid=articleid, deleted=False)
        except Article.DoesNotExist:
            return Response(
                {
                    "message": "Article not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if article.likes.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
            article.save()
            return Response(
                {
                    'status': 'UNLIKED',
                    'likes': article.likes.count()
                },
                status=status.HTTP_200_OK
            )
        else:
            article.likes.add(request.user)
            article.save()
            return Response(
                {
                    'status': 'LIKED',
                    'likes': article.likes.count()
                },
                status=status.HTTP_200_OK
            )
