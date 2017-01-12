# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from apps.users.api import AccountViewSet

urlpatterns = [

    # API Views
    url(
        regex=r'^api/accounts/cancel/$',
        view=AccountViewSet.as_view({'get': 'cancel', 'post': 'cancel_confirm'}),
        name='cancel',
    ),

    url(
        regex=r'^api/accounts/change-email/$',
        view=AccountViewSet.as_view({'post': 'change_email'}),
        name='change-email',
    ),

    url(
        regex=r'^api/accounts/change-password/$',
        view=AccountViewSet.as_view({'post': 'change_password'}),
        name='change-password',
    ),

    url(
        regex=r'^api/accounts/clear-sessions/$',
        view=AccountViewSet.as_view({'get': 'clear_sessions'}),
        name='clear-sessions',
    ),


    url(
        regex=r'^api/accounts/profile/$',
        view=AccountViewSet.as_view({'get': 'get_profile', 'put': 'update_profile'}),
        name='profile',
    ),

]