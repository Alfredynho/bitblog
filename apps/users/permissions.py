# -*- encoding:utf-8 -*-

from rest_framework.permissions import IsAuthenticated

from apps.contrib.api.permissions import BasePermissionSet, IsProfileOwner


class AccountPermissionSet(BasePermissionSet):
    get_profile_perms = [IsAuthenticated, IsProfileOwner, ]
    cancel_perms = [IsAuthenticated, ]
    cancel_confirm_perms = [IsAuthenticated, ]

    change_email_perms = [IsAuthenticated, ]
    change_password_perms = [IsAuthenticated, IsProfileOwner, ]
    update_profile_perms = [IsAuthenticated, IsProfileOwner, ]

    clear_sessions_perms = [IsAuthenticated, IsProfileOwner, ]
    logout_perms = [IsAuthenticated, IsProfileOwner, ]