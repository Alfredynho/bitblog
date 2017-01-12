# -*- encodign:utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.db import transaction

# Third part imports
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin

# Project imports
from apps.contrib.api import codes
from apps.contrib.api.exceptions import ValidationError
from apps.contrib.format.strings import get_uuid, get_lapse
from apps.credentials import messaging
from apps.credentials.transactions import do_confirm_register, do_reset_password
from apps.users.models import User, UserAction
from apps.users.serializers import UserSerializer

from apps.credentials.models import PlatformApp
from apps.credentials.permissions import AuthPermissionSet
from apps.credentials.serializers import (
    EmailOrUsernameSerializer,
    TokenSerializer,
    RegisterSerializer,
    UsernameSerializer,
    ConfirmResetPasswordSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    RevokeTokenSerializer,
    TokenResponseSerializer,
    FormattedResponseSerializer,
    EmailSerializer)

from .signals import user_registered as user_registered_signal


class AuthViewSet(ViewSet):
    permission_classes = (AuthPermissionSet,)

    @staticmethod
    def is_user_already_registered(data):
        try:
            email = data["email"]
        except Exception as e:
            email = None

        try:
            username = data["username"]
        except Exception as e:
            username = None

        if username and User.objects.filter(username=username):
            return True, _("Username is already in use.")
        if email and User.objects.filter(email=email):
            return True, _("Email is already in use.")
        return False, None

    @transaction.atomic
    def register(self, request):
        """
        # Register  a new user.

            NOTE. the 'photo' param is required only in this documentation.
        ---
        request_serializer: RegisterSerializer
        response_serializer: UserSerializer
        parameters_strategy: merge
        consumes:
            - application/json

        produces:
            - application/json
        """

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = PlatformApp.objects.get(
            client_id=serializer.data["client_id"],
            client_secret=serializer.data["client_secret"],
        )

        #  ------------------------------------------------------------------------------
        #     ADD application perms in here
        #  ------------------------------------------------------------------------------

        _data = serializer.data.copy()
        del _data["client_id"]
        del _data["client_secret"]
        del _data["password"]

        registered, reason = self.is_user_already_registered(_data)

        if not registered:
            # Create user
            user = User(**_data)
            user.is_staff = False

            # Set activate
            user.is_active = not application.has_confirmation

            # Set password
            user.set_password(serializer.data["password"])
            user.save()

            action = UserAction(
                user=user,
                type=UserAction.ACTION_ENABLE_ACCOUNT,
            )

            action.token=get_uuid()
            action.creation_date, action.expiration_date = get_lapse()
            action.save()

            # Send email
            if application.has_confirmation:
                messaging.send_account_activation(request, action)
            else:
                messaging.send_welcome(request, action)

            user_registered_signal.send(
                sender=user.__class__, user=user)

            return Response(
                UserSerializer(user, many=False).data,
                status=status.HTTP_201_CREATED
            )

        else:
            raise ValidationError(
                detail=reason,
                code=codes.REGISTERED_USER,
            )

    def send_confirmation(self, request):
        """
        # Send account confirmation to an inactive user by email or username.
        ---
        request_serializer: EmailOrUsernameSerializer
        response_serializer: FormattedResponseSerializer
        """

        serializer = EmailOrUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        eou = serializer.data["email_or_username"]
        user = User.objects.get(Q(username=eou) | Q(email=eou))

        action_exist = UserAction.objects.filter(
            user=user,
            type=UserAction.ACTION_ENABLE_ACCOUNT,
        ).exists()

        if action_exist:
            action = UserAction.objects.get(
                user=user,
                type=UserAction.ACTION_ENABLE_ACCOUNT,
            )
        else:
            action = UserAction(
                user=user,
                type=UserAction.ACTION_ENABLE_ACCOUNT,
            )

        action.token=get_uuid()
        action.creation_date, action.expiration_date  = get_lapse()
        action.save()

        user.save()
        messaging.send_account_activation(request, action)

        user_registered_signal.send(sender=user.__class__, user=user)

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def confirm_register(self, request):
        """
        # Activate an user account by confirmation token.
        ---
        request_serializer: TokenSerializer
        response_serializer: FormattedResponseSerializer
        """
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data["token"]
        return do_confirm_register(request, token=token, inner=False)

    def check_email(self, request):
        """
        # Check if an email is available
        ---
        request_serializer: EmailSerializer
        response_serializer: FormattedResponseSerializer
        """
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        is_used_email = User.objects.filter(email=email).exists()

        if is_used_email:
            raise ValidationError(
                detail=_("Este correo esta siendo usado por otro usuario"),
                code=codes.REGISTERED_USER,
            )
        else:
            return Response(
                {"detail": _("Correo Electrónico disponible")},
                status=status.HTTP_200_OK,
            )

    def check_username(self, request):
        """
        # Check if an username is available
        ---
        request_serializer: UsernameSerializer
        response_serializer: FormattedResponseSerializer
        """
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        is_used_username = User.objects.filter(username=username).exists()

        if is_used_username:
            raise ValidationError(
                detail=_("Este Nombre de Usuario esta siendo usado"),
                code=codes.REGISTERED_USER,
            )
        else:
            return Response(
                {"detail": _("Nombre de Usuario disponible")},
                status=status.HTTP_200_OK,
            )

    def reset_password(self, request):
        """
        # Send password reset token to user by username or email.
        ---
        request_serializer: EmailOrUsernameSerializer
        response_serializer: FormattedResponseSerializer
        """
        serializer = EmailOrUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eou = serializer.data['email_or_username']
        user = User.objects.get(Q(username=eou) | Q(email=eou))

        if user.is_active:
            action_exist = UserAction.objects.filter(
                user=user, type=UserAction.ACTION_RESET_PASSWORD).exists()
            if action_exist:
                action = UserAction.objects.get(user=user, type=UserAction.ACTION_RESET_PASSWORD)
            else:
                action = UserAction(user=user, type=UserAction.ACTION_RESET_PASSWORD)
            action.token = get_uuid()
            action.creation_date, action.expiration_date  = get_lapse()
            action.save()
            messaging.send_reset_password(request, action)
            return Response(
                {"detail": _("Se ha enviado un correo para restaurar contraseña")},
                status=status.HTTP_201_CREATED,
            )
        else:
            raise ValidationError(
                detail=_("La cuenta de este usuario esta inactiva"),
                code=codes.INACTIVE_ACCOUNT,
            )

            
    def confirm_reset_password(self, request):
        """
        # Reset password from password reset token.
        ---
        request_serializer: ConfirmResetPasswordSerializer
        response_serializer: FormattedResponseSerializer
        """
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data["token"]
        return do_reset_password(request, token=token, password=serializer.data["password"])


class TokenViewSet(OAuthLibMixin, ViewSet):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def get_response_token(self, request):
        url, headers, body, status = self.create_token_response(request)
        response = HttpResponse(content=body, status=status)
        return self.make_response(response, headers)

    @staticmethod
    def make_response(response, headers):
        for k, v in headers.items():
            response[k] = v
        return response

    def token(self, request):
        """
        # Endpoint to provide access tokens to authentication flow.
        ---
        request_serializer: LoginSerializer
        response_serializer: TokenResponseSerializer
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(Q(username=serializer.data["login"]) | Q(email=serializer.data["login"]))

        if request.content_type == 'application/x-www-form-urlencoded':
            if not request.POST._mutable:
                mutable = request.POST._mutable
                request.POST._mutable = True
                request.data["grant_type"] = "password"
                request.data["username"] = user.username
                request.POST._mutable = mutable
            else:
                request.data["grant_type"] = "password"
                request.data["username"] = user.username

            return self.get_response_token(request)
        else:
            raise ValidationError(
                detail=_("Content-Type no soportado"),
                code=codes.UNSUPPORTED_CONTENT_TYPE,
            )

    def refresh(self, request):
        """
        # Endpoint to provide access token to Refresh token flow.
        ---
        request_serializer: RefreshTokenSerializer
        response_serializer: TokenResponseSerializer
        """
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.content_type == 'application/x-www-form-urlencoded':
            if not request.POST._mutable:
                mutable = request.POST._mutable
                request.POST._mutable = True
                request.data["grant_type"] = "refresh_token"
                request.POST._mutable = mutable
            else:
                request.data["grant_type"] = "refresh_token"

            return self.get_response_token(request)
        else:
            raise ValidationError(
                detail=_("Content-Type no soportado"),
                code=codes.UNSUPPORTED_CONTENT_TYPE,
            )

    def revoke(self, request):
        """
        # Endpoint to provide access token to Revoke token flow.
        ---
        request_serializer: RevokeTokenSerializer
        response_serializer: TokenResponseSerializer
        """
        serializer = RevokeTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.content_type == 'application/x-www-form-urlencoded':
            url, headers, body, status = self.create_revocation_response(request)
            response = HttpResponse(content=body or '', status=status)
            return self.make_response(response, headers)
        else:
            raise ValidationError(
                detail=_("Content-Type no soportado"),
                code=codes.UNSUPPORTED_CONTENT_TYPE,
            )
