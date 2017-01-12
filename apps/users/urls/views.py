# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from apps.users.transactions import change_email, cancel_account
from apps.users.views import (
    DashboardView, ProfileView, SettingsView,
    UserDetailView, UserUpdateView, ProfileSessionsView,
)

urlpatterns = [

    # Regular Views
    url(
        regex=r'^dashboard/$',
        view=DashboardView.as_view(),
        name='view-dashboard'
    ),

    url(
        regex=r'^profile/$',
        view=ProfileView.as_view(),
        name='view-profile'
    ),

    url(
        regex=r'^settings/$',
        view=SettingsView.as_view(),
        name='view-settings'
    ),

    url(
        regex=r'^account/(?P<username>[\w.@+-]+)/$',
        view=UserDetailView.as_view(),
        name='view-detail'
    ),

    url(
        regex=r'^account/update/$',
        view=UserUpdateView.as_view(),
        name='view-update'
    ),

    url(
        regex=r'^account/change-email/(?P<token>.*)/$',
        view=change_email,
        name="view-change-email",
    ),

    url(
        regex=r'^account/cancel-account/(?P<token>.*)/$',
        view=cancel_account,
        name="view-cancel-account",
    ),

    url(
        regex=r'^profile/sessions/$',
        view=ProfileSessionsView.as_view(),
        name='view-profile-sessions'
    ),
]
