# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from users.api import AccountViewSet
from . import views

urlpatterns = [

    url(
        regex=r'^actions/cancel/$',
        view=AccountViewSet.as_view({'get': 'cancel', 'post': 'cancel_confirm'}),
        name='cancel',
    ),

    url(
        regex=r'^actions/change-email/$',
        view=AccountViewSet.as_view({'post': 'change_email'}),
        name='change-email',
    ),


    url(
        regex=r'^actions/change-password/$',
        view=AccountViewSet.as_view({'post': 'change_password'}),
        name='change-password',
    ),

    url(
        regex=r'^actions/clear-sessions/$',
        view=AccountViewSet.as_view({'get': 'clear_sessions'}),
        name='clear-sessions',
    ),

    url(
        regex=r'^actions/logout/$',
        view=AccountViewSet.as_view({'get': 'logout'}),
        name='logout',
    ),

    url(
        regex=r'^profile/$',
        view=AccountViewSet.as_view({'get': 'get_profile', 'put': 'update_profile'}),
        name='profile',
    ),

    url(
        regex=r'^change/password/$',
        view=views.UserDetailView.as_view(),
        name='detail',
    ),


]