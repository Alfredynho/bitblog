# -*- encoding:utf-8 -*-

from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import reverse

from apps.contrib.email import make_context, send_email
from apps.contrib.format.strings import get_hostname


def send_change_email(request, action):
    path = reverse("change-email", kwargs={"token": action.token})
    subject = render_to_string(
        template_name="users/email/change_email_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="users/email/change_email_body.txt",
        context=make_context(
            request=request, user=action.user, path=path,
        )
    )
    html_body = render_to_string(
        template_name="users/email/change_email_body.html",
        context=make_context(request=request, user=action.user, path=path,)
    )

    send_email(subject, [action.user.email], text_body, html_body)


def send_change_email_success(request, action):

    subject = render_to_string(
        template_name="users/email/change_email_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="users/email/change_email_body.txt",
        context=make_context(request, action)
    )
    html_body = render_to_string(
        template_name="users/email/change_email_body.html",
        context=make_context(request, action)
    )

    send_email(subject, [action.user.email], text_body, html_body)



def change_password_realized(request, action):
    hostname = get_hostname(request)
    context = RequestContext(request=request)

    subject = render_to_string(
        template_name="users/email/change_password_success_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="users/email/change_password_success_body.txt",
        context=context
    )
    html_body = render_to_string(
        template_name="users/email/change_password_success_body.html",
        context=context
    )

    send_email(subject, [action.user.email], text_body, html_body)


def change_email_realized(request, action):
    hostname = get_hostname(request)
    context = RequestContext(request=request)

    subject = render_to_string(
        template_name="users/email/change_email_success_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="users/email/change_email_success_body.txt",
        context=context
    )
    html_body = render_to_string(
        template_name="users/email/change_email_success_body.html",
        context=context
    )

    send_email(subject, [action.user.email], text_body, html_body)



def send_cancel_account(request, action):
    path = reverse("users:view-cancel-account", kwargs={"token": action.token})
    hostname = get_hostname(request)
    data = dict()
    data["user"] = action.user
    data["action_url"] = hostname + path
    context = RequestContext(request=request, dict_=data)

    subject = render_to_string(
        template_name="users/email/cancel_account_subject.txt",
        context=None
    )
    text_body = render_to_string(
        template_name="users/email/cancel_account_body.txt",
        context=context
    )
    html_body = render_to_string(
        template_name="users/email/cancel_account_body.html",
        context=context
    )

    send_email(subject, [action.user.email], text_body, html_body)
