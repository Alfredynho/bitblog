# -*- encoding:utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from oauth2_provider.models import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from apps.contrib.api import codes
from apps.contrib.api.exceptions import PermissionDenied
from apps.contrib.api.responses import DoneResponse
from apps.contrib.format.strings import get_lapse, get_uuid
from apps.credentials.serializers import TokenSerializer
from apps.users import messaging
from apps.users.models import UserAction
from apps.users.permissions import AccountPermissionSet
from apps.users.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    EmailChangeSerializer,
)

from apps.users.transactions import do_cancel_confirm


class AccountViewSet(GenericViewSet):
    permission_classes = [AccountPermissionSet, ]
    serializer_class = UserSerializer

    def get_profile(self, request):
        """
        # Get the user profile.
        ---
        response_serializer: UserSerializer
        """
        return Response(UserSerializer(request.user, many=False).data, status=status.HTTP_200_OK)

    def change_password(self, request):
        """
        # Change the password of the current user.
        ---
        serializer: PasswordChangeSerializer
        """
        serializer = PasswordChangeSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.data["new_password"])
        user.save()

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


        messaging.change_password_realized(request, action)

        return DoneResponse(
            detail=_("Password successfully changed"),
            status=status.HTTP_201_CREATED,
            code=codes.PASSWORD_CHANGED,
        )


    def cancel(self, request):
        """
        # Init the Cancel account flow and send token for it.
        ---
        omit_serializer: true
        """
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

        action.token = get_uuid()
        action.creation_date, action.expiration_date  = get_lapse()
        action.save()
        messaging.send_cancel_account(request, action)
        return DoneResponse(
            detail=_("Se inicio el proceso de desactivación de tu cuenta revisa tu correo para finalizarlo."),
            status=status.HTTP_201_CREATED,
            code=codes.CANCEL_ACCOUNT_SENT,
        )

    def cancel_confirm(self, request):
        """
        # Confirm the account cancellation via token.
        ---
        serializer: TokenSerializer
        """
        serializer = TokenSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.data["token"]
        return do_cancel_confirm(request, token=token, inner=False)

    def update_profile(self, request, *args, **kwargs):
        """
        # Update de user profile info
        ---
        request_serializer: UserUpdateSerializer
        response_serializer: UserSerializer
        parameters_strategy: merge
        parameters:
            - name: photo
              type: file
              required: false
        """
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if "username" in serializer.data:
            user.username = serializer.data["username"]
        if "first_name" in serializer.data:
            user.first_name = serializer.data["first_name"]
        if "last_name" in serializer.data:
            user.last_name = serializer.data["last_name"]
        if "photo" in request.data:
            user.photo = request.data["photo"]
        user.save()
        return Response(UserSerializer(user, many=False).data,
                        status=status.HTTP_201_CREATED)

    def change_email(self, request):
        """
        # Change the current user email change.
        ---
        serializer: EmailChangeSerializer
        """
        serializer = EmailChangeSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.email = serializer.data["email"]
        user.save()

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


        messaging.change_email_realized(request, action)

        return DoneResponse(
            detail=_("Email successfully changed"),
            status=status.HTTP_201_CREATED,
            code=codes.EMAIL_UPDATED,
        )

    def clear_sessions(self, request):
        """
        # Clear all application sessions.
        ---
        omit_serializer: true
        """
        access_tokens = AccessToken.objects.filter(user=request.user)
        access_tokens.delete()
        return DoneResponse(
            detail=_("Sessions cleared.!"),
            code=codes.SESSIONS_CLEARED,
        )

