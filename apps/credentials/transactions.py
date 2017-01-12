# -*- encoding:utf-8 -*-

from django import forms
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _

from rest_framework import status

from apps.contrib.api import codes
from apps.contrib.api.exceptions import ValidationError
from apps.contrib.api.responses import DoneResponse
from apps.credentials import messaging
from apps.users.models import UserAction


def do_confirm_register(request, token=None, inner=False):
    action_exist = UserAction.objects.filter(
        token=token, type=UserAction.ACTION_ENABLE_ACCOUNT).exists()

    context = dict()
    context["title"] = _("Confirmación de Cuenta")

    if action_exist:
        action = UserAction.objects.get(token=token, type=UserAction.ACTION_ENABLE_ACCOUNT)

        user = action.user
        user.is_active = True
        user.save()

        messaging.send_welcome(request, action)
        action.delete()

        if inner:
            context["message"] = _("Tu cuenta ha sido activada exitosamente.")
            return render(request, 'credentials/message.html', context)

        else:
            return DoneResponse(
                detail=_("La cuenta ha sido activada!"),
                code=codes.ACCOUNT_IS_ACTIVATED,
                status=status.HTTP_201_CREATED,
            )
    else:
        if inner:
            context["message"] = _("Esta Cuenta es inválida o ya fué activada.")
            context["error"] = True
            return render(request, 'credentials/message.html', context)
        else:
            raise ValidationError(
                detail=_("Token de transacción invalido"),
                code=codes.INVALID_TRANSACTION_TOKEN
            )


def _change_password(request, action, password):
    user = action.user
    user.set_password(password)
    user.save()
    action.delete()

    messaging.send_welcome(request, action)
    action.delete()


def do_reset_password(request, token=None, password=None, inner=False):
    action_exist = UserAction.objects.filter(
                token=token, type=UserAction.ACTION_RESET_PASSWORD).exists()

    context = dict()
    context["title"] = _("Reset Password")
    if action_exist:
        action = UserAction.objects.get(
                token=token, type=UserAction.ACTION_RESET_PASSWORD)

        context["valid"] = True
        user = action.user

        if user.is_active:

            if inner:
                form = ResetPasswordForm(data=request.POST)
                if form.is_valid():
                    password = form.cleaned_data["password1"]
                    _change_password(request, action, password)
                    context["message"] = _("Password has been reseted successfully!.")
                    return render(request, 'credentials/message.html', context)
                else:
                    context["has_error"] = True
                    context["message"] = _("Passwords aren't match!")
                    return render(request, 'credentials/password_reset.html', context)
            else:
                _change_password(request, action, password)
                return DoneResponse(
                    detail=_("La Contraseña ha sido restaurada!."),
                    code=codes.PASSWORD_RESTORED,
                    status=status.HTTP_201_CREATED,
                )
        else:
            if inner:
                context["has_error"] = True
                context["message"] = _("This an inactive account!")
                return render(request, 'credentials/password_reset.html', context)
            else:
                raise ValidationError(
                    detail=_("Cuenta inactiva"),
                    code=codes.INACTIVE_ACCOUNT
                )
    else:
        if inner:
            context["has_error"] = True
            context["message"] = _("Invalid action!")
            return render(request, 'credentials/password_reset.html', context)
        else:
            raise ValidationError(
                detail=_("Token de transacción invalido"),
                code=codes.INVALID_TRANSACTION_TOKEN
            )


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2


class ResetPasswordView(View):

    def get(self, request, token=None):

        action_exist = UserAction.objects.filter(
                        token=token, type=UserAction.ACTION_RESET_PASSWORD).exists()
        context = dict()
        if action_exist:
            context["valid"] = True
            return render(request, 'account/password_reset.html', context)
        else:
            context["has_error"] = True
            context["message"] = _("Invalid action!")
            return render(request, 'account/password_reset.html', context)

    def post(self, request, token=None):
        return do_reset_password(request, token=token, inner=True)


def confirm_register(request, token=None):
    return do_confirm_register(request, token=token, inner=True)


