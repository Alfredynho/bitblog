# -*- encoding:utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.views import exception_handler

from apps.contrib.api import codes


class BaseFormattedException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Error en el servidor')
    default_code = codes.INTERNAL_SERVER_ERROR

    def __init__(self, detail, code=None, docs=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)


class ValidationError(BaseFormattedException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Error de validación')
    default_code = codes.VALIDATION_ERROR


class UnauthorizedError(BaseFormattedException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Error de Autorización')
    default_code = codes.AUTHORIZATION_ERROR


class NotFound(BaseFormattedException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Item no encontrado')
    default_code = codes.NOT_FOUND


class PermissionDenied(BaseFormattedException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Permiso denegado')
    default_code = codes.PERMISSION_DENIED


def formatted_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = exc.get_full_details()
    return response
