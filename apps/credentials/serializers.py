# -*- encoding:utf-8 -*-

import re

from django.db.models import Q
from django.core import validators
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from oauth2_provider.models import RefreshToken, AccessToken
from requests import HTTPError
from rest_framework import serializers
from allauth.socialaccount.helpers import complete_social_login

from apps.contrib.api import codes
from apps.contrib.api.exceptions import ValidationError, NotFound
from apps.credentials.models import PlatformApp
from apps.users.models import User


class CleanMixin(object):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AuthTokenSerializer(CleanMixin, serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()


class ClientIDSerializer(CleanMixin, serializers.Serializer):
    client_id = serializers.CharField(max_length=100)


class TokenSerializer(CleanMixin, serializers.Serializer):
    token = serializers.CharField(max_length=150)


class ConfirmResetPasswordSerializer(CleanMixin, serializers.Serializer):
    token = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=6)


class FormattedResponseSerializer(CleanMixin, serializers.Serializer):
    message = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)


class AppMixin(CleanMixin, serializers.Serializer):

    client_id = serializers.CharField(help_text=_("Server provided"))
    client_secret = serializers.CharField(help_text=_("Server provided"))

    def validate(self, attrs):
        attrs = super(AppMixin, self).validate(attrs)
        if not PlatformApp.objects.filter(
                client_id=attrs["client_id"],
                client_secret=attrs["client_secret"],
        ).exists():
            raise ValidationError(
                detail=_("Aplicación invalida"),
                code=codes.INVALID_APPLICATION,
            )

        return attrs


class RegisterSerializer(AppMixin, serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'client_id',
            'client_secret',
        )


class LoginSerializer(AppMixin):

    login = serializers.CharField(help_text=_("User credentials"))
    password = serializers.CharField(help_text=_("User credentials"))

    def validate(self, attrs):
        attrs = super(LoginSerializer, self).validate(attrs)

        if not User.objects.filter(Q(username=attrs["login"]) | Q(email=attrs["login"])).exists():
            raise ValidationError(
                detail=_("Credenciales invalidas"),
                code=codes.INVALID_CREDENTIALS,
            )
        else:
            user = User.objects.get(Q(username=attrs["login"]) | Q(email=attrs["login"]))
            if not user.check_password(attrs["password"]):
                raise ValidationError(
                    detail=_("Credenciales invalidas"),
                    code=codes.INVALID_CREDENTIALS,
                )

        return attrs


class BaseSocialLoginSerializer(CleanMixin, serializers.Serializer):
    access_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        """

        :param adapter: allauth.socialaccount Adapter subclass. Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :returns: A populated instance of the `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _('View is not defined, pass it as a context variable')
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_('Define adapter_class in view'))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        # Case 1: We received the access_token
        if 'access_token' in attrs:
            access_token = attrs.get('access_token')

        # Case 2: We received the authorization code
        elif 'code' in attrs:
            self.callback_url = getattr(view, 'callback_url', None)
            self.client_class = getattr(view, 'client_class', None)

            if not self.callback_url:
                raise serializers.ValidationError(
                    _('Define callback_url in view')
                )
            if not self.client_class:
                raise serializers.ValidationError(
                    _('Define client_class in view')
                )

            code = attrs.get('code')

            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope
            )
            token = client.get_access_token(code)
            access_token = token['access_token']

        else:
            raise serializers.ValidationError(_('Incorrect input. access_token or code is required.'))

        token = adapter.parse_token({'access_token': access_token})
        token.app = app

        try:
            login = self.get_social_login(adapter, app, token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)

        attrs['user'] = login.account.user

        return attrs


class SocialLoginSerializer(AppMixin, BaseSocialLoginSerializer):
    pass


class TokenResponseSerializer(CleanMixin, serializers.Serializer):
    access_token = serializers.CharField(help_text=_("User credentials"))
    scope = serializers.CharField(help_text=_("User credentials"))
    expires_in = serializers.IntegerField(help_text=_("User credentials"))
    refresh_token = serializers.CharField(help_text=_("User credentials"))
    token_type = serializers.CharField(help_text=_("User credentials"))


class RefreshTokenSerializer(AppMixin):
    refresh_token = serializers.CharField(help_text=_("Get from Token"))

    def validate(self, attrs):
        attrs = super(RefreshTokenSerializer, self).validate(attrs)

        if not RefreshToken.objects.filter(token=attrs["refresh_token"]).exists():
            raise ValidationError(
                detail=_("Refresh Token inválido"),
                code=codes.INVALID_REFRESH_TOKEN,
            )

        return attrs


class RevokeTokenSerializer(AppMixin):
    token = serializers.CharField(help_text=_("Get from Token"))

    def validate(self, attrs):
        attrs = super(RevokeTokenSerializer, self).validate(attrs)

        if not AccessToken.objects.filter(token=attrs["token"]).exists():
            raise ValidationError(
                detail=_("Access Token inválido"),
                code=codes.INVALID_ACCESS_TOKEN,
            )

        return attrs


class UsernameSerializer(CleanMixin, serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        validator = validators.RegexValidator(re.compile('^[\w.-]+$'), "invalid username", "invalid")

        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Required. 255 characters or fewer. Letters, numbers "
                                              "and /./-/_ characters'")
        return value


class EmailSerializer(CleanMixin, serializers.Serializer):
    email = serializers.EmailField()


class EmailOrUsernameSerializer(CleanMixin, serializers.Serializer):
    email_or_username = serializers.CharField(max_length=250)

    def validate(self, attrs):
        attrs = super(EmailOrUsernameSerializer, self).validate(attrs)
        eou = attrs["email_or_username"]
        if not User.objects.filter(Q(username=eou) | Q(email=eou)).exists():
            raise NotFound(
                detail=_("Usuario no encontrado"),
                code=codes.USER_NOT_FOUND,
            )

        return attrs

