# -*- encodign:utf-8 -*-

# Python imports
# Django imports
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.db import transaction

# Third part imports
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.models import RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin

from braces.views import CsrfExemptMixin

# Project imports
from contrib.strings import get_uuid
from oauth.transactions import do_confirm_register, do_reset_password
from users.api import get_lapse
from users.models import User, UserAction
from users.serializers import UserSerializer, EmailSerializer

from contrib import codes
from contrib.email_services import Carrier
from contrib.exceptions import WarpResponse

from oauth.backends import KeepRequestCore
from oauth.endpoints import SocialTokenServer
from oauth.models import WarpApplication
from oauth.permissions import AuthPermissionSet
from oauth.serializers import (
    EmailOrUserSerializer,
    TokenSerializer,
    RegisterSerializer,
    UsernameSerializer,
    ConfirmResetPasswordSerializer,
    GetTokenSerializer,
    RefreshTokenSerializer,
    RevokeTokenSerializer,
    ConvertTokenSerializer,
    TokenResponse,
    FormattedResponse,
)

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
        parameters:
            - name: photo
              type: file
              required: true
              paramType: form
        consumes:
            - application/json

        produces:
            - application/json
        """

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            if WarpApplication.objects.filter(
                    client_id=serializer.data["client_id"],
                    client_secret=serializer.data["client_secret"],
            ).count() == 1:

                application = WarpApplication.objects.get(
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
                    if application.category == WarpApplication.CATEGORY_WEB:
                        user.is_active = False
                    elif application.category == WarpApplication.CATEGORY_MOBILE:
                        user.is_active = True

                    # Set password
                    user.set_password(serializer.data["password"])
                    user.save()

                    action = UserAction(
                        user=user,
                        type=UserAction.ACTION_ENABLE_ACCOUNT,
                    )

                    action.token=get_uuid()
                    action.creation_date, action.expiration_date  = get_lapse()
                    action.save()

                    # Send email
                    if application.category == WarpApplication.CATEGORY_WEB:
                        Carrier.send_account_activation(request, action)

                    elif application.category == WarpApplication.CATEGORY_MOBILE:
                        Carrier.send_welcome(request, action)

                    user_registered_signal.send(
                        sender=user.__class__, user=user)

                    return Response(
                        UserSerializer(user, many=False).data,
                        status=status.HTTP_201_CREATED
                    )

                else:
                    return WarpResponse(
                        message=reason,
                        code=codes.ERROR_REGISTERED_USER,
                    )
            else:
                return WarpResponse(
                    message=_("Invalid Application"),
                    code=codes.ERROR_INVALID_APPLICATION,
                )
        else:
            return WarpResponse(
                message=_("Missing Arguments"),
                code=codes.MISSING_ARGS,
            )

    def send_confirmation(self, request):
        """
        # Send account confirmation to an inactive user by email or username.
        ---
        request_serializer: EmailOrUserSerializer
        response_serializer: FormattedResponse
        """

        serializer = EmailOrUserSerializer(data=request.data)

        if serializer.is_valid():
            eou = serializer.data["email_or_user"]

            if User.objects.filter(Q(username=eou) | Q(email=eou)).count() == 1:

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
                Carrier.send_account_activation(request, action)

                user_registered_signal.send(sender=user.__class__, user=user)

                return WarpResponse(
                    message=_("Account Confirmation has been sent"),
                    code=codes.SUCCESS_REGISTER_CONFIRMATION_SENT,
                    status_code=status.HTTP_201_CREATED,
                )

            else:
                return WarpResponse(
                    message=_("Nonexistent User !"),
                    code=codes.ERROR_NONEXISTENT_ACCOUNT,
                    status_code=status.HTTP_404_NOT_FOUND,
                )
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def confirm_register(self, request):
        """
        # Activate an user account by confirmation token.
        ---
        request_serializer: TokenSerializer
        response_serializer: FormattedResponse
        """
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.data["token"]
            return do_confirm_register(request, token=token, inner=False)
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def check_email(self, request):
        """
        # Check if an email is available
        ---
        request_serializer: EmailSerializer
        response_serializer: FormattedResponse
        """
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            is_used_email = User.objects.filter(email=email).exists()

            if is_used_email:
                return WarpResponse(
                    message=_("Email is used another user"),
                    code=codes.STATUS_REGISTERED_USER,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return WarpResponse(
                    message=_("Email is available"),
                    code=codes.STATUS_AVAILABLE_EMAIL,
                    status_code=status.HTTP_200_OK,
                )
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def check_username(self, request):
        """
        # Check if an username is available
        ---
        request_serializer: UsernameSerializer
        response_serializer: FormattedResponse
        """
        serializer = UsernameSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data['username']
            is_used_username = User.objects.filter(username=username).exists()

            if is_used_username:
                return WarpResponse(
                    message=_("Email is used another user"),
                    code=codes.STATUS_REGISTERED_USER,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return WarpResponse(
                    message=_("Email is available"),
                    code=codes.STATUS_AVAILABLE_USERNAME,
                    status_code=status.HTTP_200_OK,
                )
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def reset_password(self, request):
        """
        # Send password reset token to user by username or email.
        ---
        request_serializer: EmailOrUserSerializer
        response_serializer: FormattedResponse
        """

        serializer = EmailOrUserSerializer(data=request.data)
        if serializer.is_valid():
            eou = serializer.data['email_or_user']

            if User.objects.filter(Q(username=eou) | Q(email=eou)).exists():
                user = User.objects.get(Q(username=eou) | Q(email=eou))

                if user.is_active:

                    action_exist = UserAction.objects.filter(
                        user=user, type=UserAction.ACTION_RESET_PASSWORD).exists()

                    if action_exist:
                        action = UserAction.objects.get(user=user, type=UserAction.ACTION_RESET_PASSWORD)
                    else:
                        action = UserAction(user=user, type=UserAction.ACTION_RESET_PASSWORD)

                    action.token=get_uuid()
                    action.creation_date, action.expiration_date  = get_lapse()
                    action.save()

                    Carrier.send_reset_password(request, action)

                    return WarpResponse(
                        message=_("Reset password message sent. !"),
                        code=codes.SUCCESS_RESET_PASSWORD_SENT,
                        status_code=status.HTTP_201_CREATED,
                    )
                else:
                    return WarpResponse(
                        message=_("This account is inactive !"),
                        code=codes.ERROR_INACTIVE_ACCOUNT,
                    )

            else:
                return WarpResponse(
                    message=_("Non existent user !"),
                    code=codes.ERROR_NONEXISTENT_ACCOUNT,
                    status_code=status.HTTP_404_NOT_FOUND,
                )
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def confirm_reset_password(self, request):
        """
        # Reset password from password reset token.
        ---
        request_serializer: ConfirmResetPasswordSerializer
        response_serializer: FormattedResponse
        """
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data["token"]
            return do_reset_password(request, token=token, password=serializer.data["password"])
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)


# ~ OAuth 2
# -----------
def check_app(id, secret):
    return WarpApplication.objects.filter(client_id=id, client_secret=secret).exists()


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
        request_serializer: GetTokenSerializer
        response_serializer: TokenResponse
        """
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():

            client_id = serializer.data["client_id"]
            client_secret = serializer.data["client_secret"]
            eou = serializer.data["email_or_user"]
            password = serializer.data["password"]

            if check_app(client_id, client_secret):
                if User.objects.filter(Q(username=eou) | Q(email=eou)).exists():
                    user = User.objects.get(Q(username=eou) | Q(email=eou))

                    if user.check_password(password):

                        # This is a hack to documentations works
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

                return WarpResponse(
                    message=_("Invalid user credentials"),
                    code=codes.ERROR_INVALID_USER_CREDENTIALS,
                )
            else:
                return WarpResponse(
                    message=_("Invalid client application"),
                    code=codes.ERROR_INVALID_APPLICATION,
                )
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def refresh(self, request):
        """
        # Endpoint to provide access token to Refresh token flow.
        ---
        request_serializer: RefreshTokenSerializer
        response_serializer: TokenResponse
        """
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():

            # This is a hack to documentations works
            client_id = serializer.data["client_id"]
            client_secret = serializer.data["client_secret"]
            token = serializer.data["refresh_token"]

            if check_app(client_id, client_secret):
                if RefreshToken.objects.filter(token=token).exists():
                    if not request.POST._mutable:
                        mutable = request.POST._mutable
                        request.POST._mutable = True
                        request.data["grant_type"] = "refresh_token"
                        request.POST._mutable = mutable
                    else:
                        request.data["grant_type"] = "refresh_token"
                else:
                    return WarpResponse(
                        message=_("Invalid refresh token"),
                        code=codes.ERROR_INVALID_REFRESH_TOKEN
                    )
                return self.get_response_token(request)
            else:
                return WarpResponse(code=codes.ERROR_INVALID_APPLICATION)
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)

    def revoke(self, request):
        """
        # Endpoint to provide access token to Revoke token flow.
        ---
        request_serializer: RevokeTokenSerializer
        response_serializer: TokenResponse
        """
        serializer = RevokeTokenSerializer(data=request.data)
        if serializer.is_valid():

            client_id = serializer.data["client_id"]
            client_secret = serializer.data["client_secret"]
            token = serializer.data["token"]

            if check_app(client_id, client_secret):
                if RefreshToken.objects.filter(token=token).exists():
                    url, headers, body, status = self.create_revocation_response(request)
                    response = HttpResponse(content=body or '', status=status)
                    return self.make_response(response, headers)
                else:
                    return WarpResponse(
                        message=_("Invalid refresh token"),
                        code=codes.ERROR_INVALID_TOKEN
                    )
            else:
                return WarpResponse(code=codes.ERROR_INVALID_APPLICATION)
        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)


class ConvertTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    server_class = SocialTokenServer
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = KeepRequestCore

    def post(self, request, *args, **kwargs):
        """
        # Endpoint to convert Social Acces Token for Django Acces Token
        ---
        request_serializer: ConvertTokenSerializer
        response_serializer: TokenResponse
        """
        serializer = ConvertTokenSerializer(data=request.data)

        if serializer.is_valid():

            client_id = serializer.data["client_id"]
            client_secret = serializer.data["client_secret"]

            if check_app(client_id, client_secret):

                # This is a hack to documentations works
                if not request.POST._mutable:
                    mutable = request.POST._mutable
                    request.POST._mutable = True
                    request.data["grant_type"] = "convert_token"
                    request.POST._mutable = mutable
                else:
                    request.data["grant_type"] = "convert_token"

                url, headers, body, status = self.create_token_response(request)
                response = HttpResponse(content=body, status=status)
                return TokenViewSet.make_response(response, headers)
            else:
                return WarpResponse(code=codes.ERROR_INVALID_APPLICATION)

        else:
            return WarpResponse(code=codes.ERROR_MISSING_ARGUMENTS)




