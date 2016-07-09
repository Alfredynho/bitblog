# -*- encoding:utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from oauth2_provider.models import AccessToken

from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import GenericViewSet

from contrib import codes
from contrib.email_services import Carrier
from contrib.exceptions import WarpResponse
from contrib.strings import get_lapse, get_uuid
from oauth.serializers import TokenSerializer
from users.models import User, UserAction
from users.permissions import AccountPermissionSet
from users.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
)
from users.transactions import do_cancel_confirm, do_change_email


class AccountViewSet(GenericViewSet):
    permission_classes = [AccountPermissionSet, ]
    serializer_class = UserSerializer

    def get_profile(self, request):
        """
        # Get the user profile.
        ---
        response_serializer: UserSerializer
        """
        if request.user.is_authenticated():
            return Response(UserSerializer(request.user, many=False).data, status=status.HTTP_200_OK)
        else:
            return WarpResponse(
                message=_("Credentials aren't provided!"),
                status_code=status.HTTP_401_UNAUTHORIZED,
                code=codes.CREDENTIALS_NOT_PROVIDED,
            )

    def change_password(self, request):
        """
        # Change the password of the current user.
        ---
        serializer: PasswordChangeSerializer
        """

        serializer = PasswordChangeSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()

            return WarpResponse(
                message=_("Password successfully changed"),
                status_code=status.HTTP_201_CREATED,
                code=codes.SUCCESS_PASSWORD_CHANGED,
            )
        return WarpResponse(
                message=_("Passwords aren't mismatch"),
                status_code=status.HTTP_400_BAD_REQUEST,
                code=codes.PASSWORDS_ARENOT_MISMATCH,
            )

    def cancel(self, request):
        """
        # Init the Cancel account flow and send token for it.
        ---
        omit_serializer: true
        """
        if request.user and request.user.is_authenticated():
            action_exist = UserAction.objects.filter(
                user=request.user, type=UserAction.ACTION_DISABLE_ACCOUNT).exists()

            if action_exist:
                action = UserAction.objects.get(
                    user=request.user, type=UserAction.ACTION_DISABLE_ACCOUNT)
            else:
                action = UserAction(
                    user=request.user,
                    type=UserAction.ACTION_DISABLE_ACCOUNT
                )

            action.token=get_uuid()
            action.creation_date, action.expiration_date  = get_lapse()
            action.save()
            Carrier.send_cancel_account(request, action)

            return WarpResponse(
                message=_("Delete account action is activated, check your email to finish it."),
                status_code=status.HTTP_201_CREATED,
                code=codes.SUCCESS_CANCEL_ACCOUNT_SENT,
            )

        else:
            return WarpResponse(
                message=_("Credentials aren't provided!"),
                status_code=status.HTTP_401_UNAUTHORIZED,
                code=codes.CREDENTIALS_NOT_PROVIDED,
            )

    def cancel_confirm(self, request):
        """
        # Confirm the account cancellation via token.
        ---
        serializer: TokenSerializer
        """

        serializer = TokenSerializer(data=request.data, many=False)

        if serializer.is_valid():
            token = serializer.data["token"]
            return do_cancel_confirm(request, token=token, inner=False)
        else:
            return WarpResponse(
                message=_("Invalid arguments"),
                status_code=status.HTTP_400_BAD_REQUEST,
                code=codes.ERROR_MISSING_ARGUMENTS,
            )

    def update_profile(self, request, *args, **kwargs):
        """
        # Update de user profile info
        ---
        serializer: UserUpdateSerializer
        omit_serializer: false
        parameters_strategy: merge
        parameters:
            - name: avatar
              type: file
              required: false
        """

        user = request.user
        if user and user.is_authenticated():

            old_email = user.email
            new_email = request.data.get('email', None)

            for (key, value) in request.data.items():
                setattr(user, key, value)

            user.email = old_email
            user.save()

            if new_email is not None and new_email != old_email:
                valid_new_email = True
                duplicated_email = User.objects.filter(email=new_email).exists()

                try:
                    validate_email(new_email)
                except ValidationError:
                    valid_new_email = False

                if duplicated_email:
                    return WarpResponse(
                        message=_("This mail is being used by another user"),
                        status_code=status.HTTP_400_BAD_REQUEST,
                        code=codes.ERROR_DUPLICATED_EMAIL,
                    )
                elif not valid_new_email:
                    return WarpResponse(
                        message=_("Not valid email"),
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        code=codes.ERROR_INVALID_EMAIL,
                    )

                user.email = old_email
                user.save()

                action_exist = UserAction.objects.filter(user=user, type=UserAction.ACTION_CHANGE_EMAIL).exists()

                if action_exist:
                    action = UserAction.objects.get(user=user, type=UserAction.ACTION_CHANGE_EMAIL)
                else:
                    action = UserAction(
                        user=user,
                        type=UserAction.ACTION_CHANGE_EMAIL
                    )

                action.token=get_uuid()
                action.value=new_email
                action.creation_date, action.expiration_date  = get_lapse()
                action.save()

                Carrier.send_change_email(request, action)

            return Response(UserSerializer(user, many=False).data,
                            status=status.HTTP_201_CREATED)

        else:
            return WarpResponse(
                message=_("Credentials aren't provided!"),
                status_code=status.HTTP_401_UNAUTHORIZED,
                code=codes.CREDENTIALS_NOT_PROVIDED,
            )

    def change_email(self, request):
        """
        # Change the current user email change.
        ---
        serializer: TokenSerializer
        """

        serializer = TokenSerializer(data=request.data, many=False)
        if serializer.is_valid():
            token = serializer.data["token"]
            return do_change_email(request, token=token, inner=False)

        else:
            return WarpResponse(
                message=_("Invalid arguments"),
                status_code=status.HTTP_400_BAD_REQUEST,
                code=codes.ERROR_MISSING_ARGUMENTS,
            )

    def clear_sessions(self, request):
        """
        # Clear all application sessions.
        ---
        omit_serializer: true
        """

        access_tokens = AccessToken.objects.filter(user=request.user)
        access_tokens.delete()

        return WarpResponse(
            message=_("Sessions cleared.!"),
            code=codes.SUCCESS_SESSIONS_CLEARED,
            status_code=status.HTTP_200_OK,
        )

    def logout(self, request):
        """
        # Clear the current session.
        ---
        omit_serializer: true
        """

        if request.user and request.user.is_authenticated() and request.META["HTTP_AUTHORIZATION"]:
            token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]

            access_tokens = AccessToken.objects.filter(
                user=request.user, token=token)
            access_tokens.delete()

            return WarpResponse(
                message=_("Logout complete!"),
                code=codes.SUCCESS_LOGOUT,
                status_code=status.HTTP_200_OK,
            )

        else:
            return WarpResponse(
                message=_("Credentials aren't provided!"),
                status_code=status.HTTP_401_UNAUTHORIZED,
                code=codes.CREDENTIALS_NOT_PROVIDED,
            )