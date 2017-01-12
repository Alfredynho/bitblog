# -*- encoding:utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from rest_framework import status

from apps.contrib.api import codes
from apps.contrib.api.exceptions import ValidationError
from apps.contrib.api.responses import DoneResponse
from apps.users.models import UserAction

from django.utils.translation import ugettext_lazy as _


def do_change_email(request, token=None, inner=False):
    action_exist = UserAction.objects.filter(token=token, type=UserAction.ACTION_CHANGE_EMAIL).exists()

    context = dict()
    context["title"] = _("Change email")

    if action_exist:
        action = UserAction.objects.get(token=token, type=UserAction.ACTION_CHANGE_EMAIL)
        action.user.email = action.value
        action.user.save()

        action.delete()

        if inner:
            context["message"] = _("Tu correo ha sido actualizado con éxito")
            return render(request, 'credentials/message.html', context)
        else:
            return DoneResponse(
                detail=_("Correo actualizado con exito!"),
                status=status.HTTP_201_CREATED,
                code=codes.EMAIL_UPDATED,
            )
    else:
        if inner:
            context["message"] = _("Acción Invalida!")
            context["error"] = True
            return render(request, 'credentials/message.html', context)
        else:
            raise ValidationError(
                detail=_("Token de transacción invalido"),
                code=codes.INVALID_TRANSACTION_TOKEN
            )


def do_cancel_confirm(request, token=None, inner=False):
    action_exist = UserAction.objects.filter(
        token=token, type=UserAction.ACTION_DISABLE_ACCOUNT).exists()

    context = dict()
    context["title"] = _("Cancel account")

    if action_exist:
        action = UserAction.objects.get(
            token=token, type=UserAction.ACTION_DISABLE_ACCOUNT)

        action.user.is_active = False
        action.user.save()
        if not settings:
            action.user.delete()
        action.delete()

        message = _("Tu cuenta ha sido eliminada correctamente")
        if inner:
            context["message"] = message
            return render(request, 'credentials/message.html', context)
        else:
            return DoneResponse(
                detail=message,
                status=status.HTTP_201_CREATED,
                code=codes.ACCOUNT_DISABLED,
            )
    else:
        message = _("Acción inválida")
        if inner:
            context["message"] = message
            context["error"] = True
            return render(request, 'credentials/message.html', context)
        else:
            raise ValidationError(
                detail=message,
                code=codes.INVALID_ACTION
            )


def change_email(request, token=None):
    return do_change_email(request, token=token, inner=True)


def cancel_account(request, token=None):
    return do_cancel_confirm(request, token=token, inner=True)
