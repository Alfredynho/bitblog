# -*- encoding:utf-8 -*-

from contrib.mixins import UsernameValidationMixin
from users.models import User


from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers



class AuthTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()




# --------------- CLEANED --------------

class ClientIDSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=100)

class EmailSerializer(serializers.Serializer):
    email_or_user = serializers.CharField(max_length=150)


class UsernameSerializer(UsernameValidationMixin, serializers.Serializer):
    username = serializers.CharField(max_length=30)


class EmailOrUserSerializer(serializers.Serializer):
    email_or_user = serializers.CharField(max_length=150)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=150)


class ConfirmResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=6)


class RegisterSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(help_text=_("Server provided"))
    client_secret = serializers.CharField(help_text=_("Server provided"))
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'photo',
            'phone',

            'client_id',
            'client_secret',
        )

class GetTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(help_text=_("Server provided"))
    client_secret = serializers.CharField(help_text=_("Server provided"))
    email_or_user = serializers.CharField(help_text=_("User credentials"))
    password = serializers.CharField(help_text=_("User credentials"))


class RefreshTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(help_text=_("Server provided"))
    client_secret = serializers.CharField(help_text=_("Server provided"))
    refresh_token = serializers.CharField(help_text=_("Get from Token"))


class RevokeTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(help_text=_("Server provided"))
    client_secret = serializers.CharField(help_text=_("Server provided"))
    token = serializers.CharField(help_text=_("Get from Token"))


class ConvertTokenSerializer(serializers.Serializer):
    BACKEND_CHOICES = [
        ("facebook", "facebook"),
        ("google", "google"),
        ("twitter", "twitter"),
    ]
    client_id = serializers.CharField(help_text=_("Server provided"))
    client_secret = serializers.CharField(help_text=_("Server provided"))
    backend = serializers.ChoiceField(help_text=_("Social Network"), choices=BACKEND_CHOICES)
    token = serializers.CharField(help_text=_("Get from Social Network"))


class TokenResponse(serializers.Serializer):
    access_token = serializers.CharField(help_text=_("User credentials"))
    scope = serializers.CharField(help_text=_("User credentials"))
    expires_in = serializers.IntegerField(help_text=_("User credentials"))
    refresh_token = serializers.CharField(help_text=_("User credentials"))
    token_type = serializers.CharField(help_text=_("User credentials"))

class FormattedResponse(serializers.Serializer):
    message = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)
    status_code = serializers.CharField(required=False)
    docs = serializers.CharField(required=False)
    dev_message = serializers.CharField(required=False)