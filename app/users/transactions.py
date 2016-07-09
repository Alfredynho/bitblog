from django.conf import settings
from django.shortcuts import render
from rest_framework import status

from contrib import codes
from contrib.exceptions import WarpResponse
from users.models import UserAction

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
            context["message"] = _("The email has been canceled successfully.")
            return render(request, 'transactions/message.html', context)
        else:
            return WarpResponse(
                message=_("Email Changed successfully!"),
                status_code=status.HTTP_201_CREATED,
                code=codes.SUCCESS_EMAIL_UPDATED,
            )
    else:
        if inner:
            context["message"] = _("Invalid action!")
            context["error"] = True
            return render(request, 'transactions/message.html', context)
        else:
            return WarpResponse(
                message=_("Invalid email token"),
                status_code=status.HTTP_400_BAD_REQUEST,
                code=codes.ERROR_INVALID_TOKEN,
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
        if settings.DELETE_ACCOUNT_AFTER_DISABLE:
            action.user.delete()
        action.delete()

        if inner:
            context["message"] = _("This account has been canceled correctly.")
            return render(request, 'transactions/message.html', context)
        else:
            return WarpResponse(
                message=_("Your Accound has been disabled!"),
                status_code=status.HTTP_201_CREATED,
                code=codes.SUCCESS_ACCOUNT_DISABLED,
            )
    else:
        if inner:
            context["message"] = _("Invalid action!")
            context["error"] = True
            return render(request, 'transactions/message.html', context)
        else:
            return WarpResponse(
                message=_("Invalid action or Invalid Token!"),
                status_code=status.HTTP_400_BAD_REQUEST,
                code=codes.ERROR_INVALID_ACTION,
            )


def change_email(request, token=None):
    return do_change_email(request, token=token, inner=True)


def cancel_account(request, token=None):
    return do_cancel_confirm(request, token=token, inner=True)