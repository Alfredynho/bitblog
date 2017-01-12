# -*- encoding:utf-8 -*-

from datetime import timedelta

from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from oauth2_provider.models import AccessToken, get_application_model, RefreshToken
from oauth2_provider.views.mixins import OAuthLibMixin
from oauthlib.oauth2.rfc6749.tokens import random_token_generator

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.contrib.api import codes
from apps.contrib.api.exceptions import ValidationError
from apps.contrib.format.date import now
from apps.credentials.serializers import SocialLoginSerializer


class GetNumberPhoneView(TemplateView):
    template_name = "credentials/get_number.html"


class SocialLoginView(OAuthLibMixin, GenericAPIView):
    # server_class = SocialTokenServer
    # validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    # oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
    # RequestValidator

    permission_classes = (AllowAny,)
    app_model = get_application_model()
    serializer_class = SocialLoginSerializer

    def create_token(self, request, app, user):
        """Create a BearerToken, by default without refresh token."""

        access_token = AccessToken.objects.get_or_create(
            user=user, application=app, expires=now() + timedelta(days=365),
            token=random_token_generator(request), scope="read write")[0]
        access_token.save()

        refresh_token = RefreshToken.objects.get_or_create(
            user=user, application=app, token=random_token_generator(request),
            access_token=access_token)[0]
        refresh_token.save()

        token = {
            "token_type": "Bearer",
            "refresh_token": refresh_token.token,
            "scope": access_token.scope,
            "access_token": access_token.token,
            "expires_in": 36000,
        }
        return token

    def login(self):
        self.user = self.serializer.validated_data['user']
        # django_login(self.request, self.user)

    def get_response(self, request):
        user = self.user

        app = self.app_model.objects.get(
            client_id=self.serializer.data["client_id"],
            client_secret=self.serializer.data["client_secret"])

        response = self.create_token(request, app, user)
        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/x-www-form-urlencoded':
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)

            exist_app = self.app_model.objects.filter(
                client_id=self.serializer.data["client_id"],
                client_secret=self.serializer.data["client_secret"]).exists()

            if exist_app:
                self.login()
                return self.get_response(request)

            else:
                raise ValidationError(
                    detail=_("Aplicacion invalida"),
                    code=codes.INVALID_APPLICATION
                )
        else:
            raise ValidationError(
                detail=_("Content-Type no soportado"),
                code=codes.UNSUPPORTED_CONTENT_TYPE,
            )


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter







