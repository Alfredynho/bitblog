# -*- encoding:utf-8 -*-

from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import reverse

from apps.contrib.email import send_email
from apps.contrib.format.strings import get_hostname


def send_account_activation(request, action):
    path = reverse("credentials:account-activation", kwargs={"token": action.token})
    hostname = get_hostname(request)
    data = dict()
    data["user"] = action.user
    data["activate_url"] = hostname + path
    context = RequestContext(request=request, dict_=data)

    subject = render_to_string(
        template_name="account/email/email_confirmation_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="account/email/email_confirmation_message.txt",
        context=context
    )
    html_body = render_to_string(
        template_name="account/email/email_confirmation_message.html",
        context=context
    )

    send_email(subject, [action.user.email], text_body, html_body)


def send_welcome(request, action):
    hostname = get_hostname(request)
    data = dict()
    data["action_url"] = hostname
    context = RequestContext(request=request, dict_=data)

    subject = render_to_string(
        template_name="credentials/email/account_welcome_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="credentials/email/account_welcome_message.txt",
        context=context
    )
    html_body = render_to_string(
        template_name="credentials/email/account_welcome_message.html",
        context=context
    )

    send_email(subject, [action.user.email], text_body, html_body)


def send_reset_password(request, action):
    path = reverse("credentials:reset-password", kwargs={"token": action.token})
    hostname = get_hostname(request)
    data = dict()
    data["user"] = action.user
    data["password_reset_url"] = hostname + path
    context = RequestContext(request=request, dict_=data)

    subject = render_to_string(
        template_name="account/email/password_reset_key_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="account/email/password_reset_key_message.txt",
        context=context
    )
    html_body = render_to_string(
        template_name="account/email/password_reset_key_message.html",
        context=context
    )

    send_email(subject, [action.user.email], text_body, html_body)
