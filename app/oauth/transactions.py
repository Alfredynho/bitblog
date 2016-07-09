from django import forms
from django.shortcuts import render
from django.views.generic import FormView, View
from rest_framework import status

from contrib import codes
from contrib.email_services import Carrier
from contrib.exceptions import WarpResponse
from users.models import UserAction
from django.utils.translation import ugettext_lazy as _


def do_confirm_register(request, token=None, inner=False):
    action_exist = UserAction.objects.filter(
        token=token, type=UserAction.ACTION_ENABLE_ACCOUNT).exists()

    context = dict()
    context["title"] = _("Account Activation")

    if action_exist:
        action = UserAction.objects.get(token=token, type=UserAction.ACTION_ENABLE_ACCOUNT)

        user = action.user
        user.is_active = True
        user.save()

        Carrier.send_welcome(request, action)
        action.delete()

        if inner:
            context["message"] = _("Your account has been activated successfully.")
            return render(request, 'transactions/message.html', context)

        else:
            return WarpResponse(
                message=_("Account has been activated!"),
                code=codes.ERROR_INVALID_TOKEN,
                status_code=status.HTTP_201_CREATED,
            )
    else:
        if inner:
            context["message"] = _("This account is invalid.")
            context["error"] = True
            return render(request, 'transactions/message.html', context)
        else:
            return WarpResponse(
                message=_("Invalid confirmation Token!"),
                code=codes.ERROR_INVALID_TOKEN,
            )


def _change_password(request, action, password):
    user = action.user
    user.set_password(password)
    user.save()
    Carrier.send_reset_password_success(request, action)
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
                    return render(request, 'transactions/message.html', context)
                else:
                    context["has_error"] = True
                    context["message"] = _("Passwords aren't match!")
                    return render(request, 'transactions/reset_password.html', context)
            else:
                _change_password(request, action, password)
                return WarpResponse(
                    message= _("Password has been reseted successfully!."),
                    code=codes.SUCCESS_REGISTER_CONFIRMATION_SENT,
                    status_code=status.HTTP_200_OK,
                )
        else:
            if inner:
                context["has_error"] = True
                context["message"] = _("This an inactive account!")
                return render(request, 'transactions/reset_password.html', context)
            else:
                return WarpResponse(
                    message=_("This account is inactive !"),
                    code=codes.ERROR_INACTIVE_ACCOUNT,
                )
    else:
        if inner:
            context["has_error"] = True
            context["message"] = _("Invalid action!")
            return render(request, 'transactions/reset_password.html', context)
        else:
            return WarpResponse(
                message=_("Invalid Token.!"),
                code=codes.ERROR_INVALID_TOKEN
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
            return render(request, 'transactions/reset_password.html', context)
        else:
            context["has_error"] = True
            context["message"] = _("Invalid action!")
            return render(request, 'transactions/reset_password.html', context)

    def post(self, request, token=None):
        return do_reset_password(request, token=token, inner=True)


def confirm_register(request, token=None):
    return do_confirm_register(request, token=token, inner=True)


