# -*- encoding:utf-8 -*-

import hashlib

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from users.models import User
from sorl.thumbnail.shortcuts import get_thumbnail
from django.conf import settings


# PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length

PASSWORD_MAX_LENGTH = 10
user_read_only_fields = (
    'id', 'username', 'date_joined', 'last_login', 'new_email',
    'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
    'email_token', 'token', 'groups', 'user_permissions',
)

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'photo',
            'phone',
        ]

        read_only_fields = user_read_only_fields


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    class Meta:
        model = User

        fields = [
            'first_name', 'last_name',
            'email', 'photo', 'phone',
        ]

        read_only_fields = user_read_only_fields


class PasswordChangeSerializer(serializers.Serializer):
    """
    Change password serializer
    """
    current_password = serializers.CharField(
        help_text=_('Current Password'),
        max_length=PASSWORD_MAX_LENGTH,
        required=False  # optional because users subscribed from social network won't have a password set
    )
    password1 = serializers.CharField(
        help_text=_('New Password'),
        max_length=PASSWORD_MAX_LENGTH
    )
    password2 = serializers.CharField(
        help_text=_('New Password (confirmation)'),
        max_length=PASSWORD_MAX_LENGTH
    )

    def update(self, instance, validated_data):
        """ change password """
        if instance is not None:
            instance.change_password(validated_data.get('password2'))
        return instance

    def create(self, validated_data):
        return User(**validated_data)

    def validate_current_password(self, value):
        """
        current password check
        """
        if self.instance.has_usable_password() and not self.instance.check_password(value):
            raise serializers.ValidationError(_('Current password is not correct'))
        return value

    def validate(self, data):
        """
        password_confirmation check
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_('Password confirmation mismatch'))
        return data

