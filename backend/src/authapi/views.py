from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from knox.models import AuthToken

from jsis.env import SERVER_DOMAIN

from .models import UserAccount
from .tokens import account_activation_token
from .serializers import LoginSerializer, DetailedUserSerializer, RegisterSerializer

# Create your views here.
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            return Response(
                {
                    "message": error.messages
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data

        return Response(
            {
                "user": DetailedUserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            return Response(
                {
                    "message": error.messages
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        token = account_activation_token.make_token(user)
        html_msg = render_to_string('authapi/email_template.html', {
                'server_domain': SERVER_DOMAIN,
                'token': token,
                'uid': user.pk,
            })

        email = EmailMultiAlternatives('[JSIS] 부산중앙고등학교 재학생인트라넷서비스 회원가입 인증 메일',
            strip_tags(html_msg),
            to=[user.email])
        email.attach_alternative(html_msg, 'text/html')
        email.send()

        return Response(
            {
                "user": DetailedUserSerializer(user, context=self.get_serializer_context()).data,
            }
        )


class UserAPI(generics.GenericAPIView):
    serializer_class = DetailedUserSerializer
    permission_classes = [ permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        user_serialized = DetailedUserSerializer(user, context=self.get_serializer_context()).data

        return Response(user_serialized)


class EmailValidationAPI(generics.GenericAPIView):
    def get(self, _request, uid, token):
        user = UserAccount.objects.get(pk=uid)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(
                {
                    "message": "Your account is activated."
                }
            )

        return Response(
            {
                "message": "Token not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )
