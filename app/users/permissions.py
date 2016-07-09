# -*- encoding:utf-8 -*-



from rest_framework.permissions import AllowAny, IsAuthenticated

from contrib.permissions import BasePermissionSet, IsProfileOwner


class AccountPermissionSet(BasePermissionSet):
    cancel_perms = [IsAuthenticated, ]
    cancel_confirm_perms = [IsAuthenticated, ]

    change_email_perms = [IsAuthenticated, ]
    get_profile_perms = [IsAuthenticated, IsProfileOwner, ]

    change_password_perms = [IsAuthenticated, IsProfileOwner, ]
    update_profile_perms = [IsAuthenticated, IsProfileOwner, ]


    clear_sessions_perms = [IsAuthenticated, IsProfileOwner, ]
    logout_perms = [IsAuthenticated, IsProfileOwner, ]
