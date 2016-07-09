# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from contrib.strings import get_hostname


def make_context(request, action=None, path=None):

    hostname = get_hostname(request)
    data = dict()

    if path:
        data["host"] = hostname + path

    if action:
        data["user"] = action.user

    context = RequestContext(request=request, dict_=data)
    return context


def send_email(subject, to, text_body, html_body):
    email = EmailMultiAlternatives(subject=subject,
                                   from_email=settings.DEFAULT_FROM_EMAIL, to=to, body=text_body)
    email.attach_alternative(html_body, "text/html")
    email.send()


class Carrier(object):
    @staticmethod
    def send_account_activation(request, action):

        if settings.MANAGE_TRANSACTIONS:
            path = reverse("account-activation", kwargs={"token": action.token})
        else:
            path = settings.ACTION_ACCOUNT_ACTIVATION

        subject = render_to_string(
            template_name="emails/account_activation-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/account_activation-body.txt",
            context=make_context(
                request=request, action=action, path=path,
            )
        )
        html_body = render_to_string(
            template_name="emails/account_activation-body.html",
            context=make_context(
                request=request, action=action, path=path,
            )
        )
        send_email(subject, [action.user.email], text_body, html_body)

    @staticmethod
    def send_welcome(request, action):

        subject = render_to_string(
            template_name="emails/account_welcome-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/account_welcome-body.txt",
            context=make_context(request, action)
        )
        html_body = render_to_string(
            template_name="emails/account_welcome-body.html",
            context=make_context(request, action)
        )
        send_email(subject, [action.user.email], text_body, html_body)

    @staticmethod
    def send_reset_password(request, action):

        if settings.MANAGE_TRANSACTIONS:
            path = reverse("reset-password", kwargs={"token": action.token})
        else:
            path = settings.ACTION_RESET_PASSWORD

        subject = render_to_string(
            template_name="emails/reset_password-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/reset_password-body.txt",
            context=make_context(
                request=request, action=action, path=path,
            )
        )
        html_body = render_to_string(
            template_name="emails/reset_password-body.html",
            context=make_context(
                request=request, action=action, path=path,
            )
        )
        send_email(subject, [action.user.email], text_body, html_body)

    @staticmethod
    def send_reset_password_success(request, action):

        subject = render_to_string(
            template_name="emails/reset_password_success-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/reset_password_success-body.txt",
            context=make_context(request, action)
        )
        html_body = render_to_string(
            template_name="emails/reset_password_success-body.html",
            context=make_context(request, action)
        )
        send_email(subject, [action.user.email], text_body, html_body)

    @staticmethod
    def send_change_email(request, action):

        if settings.MANAGE_TRANSACTIONS:
            path = reverse("change-email", kwargs={"token": action.token})
        else:
            path = settings.ACTION_CHANGE_EMAIL

        subject = render_to_string(
            template_name="emails/change_email-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/change_email-body.txt",
            context=make_context(
                request=request, action=action, path=path,
            )
        )
        html_body = render_to_string(
            template_name="emails/change_email-body.html",
            context=make_context(
                request=request, action=action, path=path,
            )
        )
        send_email(subject, [action.user.email], text_body, html_body)

    @staticmethod
    def send_change_email_success(request, action):

        subject = render_to_string(
            template_name="emails/change_email_success-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/change_email_success-body.txt",
            context=make_context(request, action)
        )
        html_body = render_to_string(
            template_name="emails/change_email_success-body.html",
            context=make_context(request, action)
        )
        send_email(subject, [action.user.email], text_body, html_body)

    @staticmethod
    def send_cancel_account(request, action):

        if settings.MANAGE_TRANSACTIONS:
            path = reverse("cancel-account", kwargs={"token": action.token})
        else:
            path = settings.ACTION_CANCEL_ACCOUNT

        subject = render_to_string(
            template_name="emails/cancel_account-subject.txt",
            context=None
        )
        text_body = render_to_string(
            template_name="emails/cancel_account-body.txt",
            context=make_context(request, action, path)
        )
        html_body = render_to_string(
            template_name="emails/cancel_account-body.html",
            context=make_context(request, action, path)
        )
        send_email(subject, [action.user.email], text_body, html_body)
