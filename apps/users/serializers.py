# -*- encoding:utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from apps.contrib.api import codes
from apps.contrib.api.exceptions import ValidationError
from apps.users.models import User

PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length
user_read_only_fields = (
    'id', 'username', 'date_joined', 'last_login', 'new_email',
    'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
    'email_token', 'token', 'groups', 'user_permissions',
)


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
        ]
        read_only_fields = user_read_only_fields


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = super(UserUpdateSerializer, self).validate(attrs)
        if "username" in attrs:
            if User.objects.filter(username=attrs["username"]).exists():
                raise ValidationError(
                    detail=_("Este nombre de usuario está siendo utilizado por otro usuario"),
                    code=codes.USED_USERNAME,
                )
        return attrs

    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'photo',
        ]


class CheckValidPasswordMixin(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        user = self.context["request"].user
        if user and user.is_authenticated():
            if "password" not in attrs or not user.check_password(attrs["password"]):
                raise ValidationError(
                    detail=_("La contraseña actual no es valida"),
                    code=codes.INVALID_PASSWORD
                )
        else:
            raise ValidationError(
                detail=_("No tiene credenciales para ejecutar esta acción"),
                code=codes.PERMISSION_DENIED
            )
        return attrs


class PasswordChangeSerializer(CheckValidPasswordMixin):
    """
    Change password serializer
    """
    password = serializers.CharField(
        help_text=_('Contraseña actual'),
        max_length=PASSWORD_MAX_LENGTH,
    )
    new_password = serializers.CharField(
        help_text=_('Nueva Contraseña'),
        max_length=PASSWORD_MAX_LENGTH
    )


class EmailChangeSerializer(CheckValidPasswordMixin):
    """
    Change email serializer
    """
    password = serializers.CharField(
        help_text=_('Contraseña'),
        max_length=PASSWORD_MAX_LENGTH,
    )
    email = serializers.EmailField(
        help_text=_('Nuevo Correo'),
    )

