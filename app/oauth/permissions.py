# -*- encoding:utf-8 -*-

from contrib.permissions import BasePermissionSet
from rest_framework.permissions import AllowAny


class AuthPermissionSet(BasePermissionSet):
    register_perms = [AllowAny, ]
    send_confirmation_perms = [AllowAny, ]
    confirm_register_perms = [AllowAny, ]
    get_auth_token_perms = [AllowAny, ]
    get_csrf_token_perms = [AllowAny, ]
    check_email_perms = [AllowAny, ]
    check_username_perms = [AllowAny, ]
    partial_info_perms = [AllowAny, ]
    reset_password_perms = [AllowAny, ]
    confirm_reset_password_perms = [AllowAny, ]
    validate_reset_password_perms = [AllowAny, ]

    social_auth_perms = [AllowAny, ]
