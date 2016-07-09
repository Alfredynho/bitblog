# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from social.backends.oauth import BaseOAuth2
from django.core.urlresolvers import reverse_lazy
from oauth2_provider.oauth2_backends import OAuthLibCore
from django.conf import settings


PROPRIETARY_BACKEND_NAME = getattr(
    settings,
    'PROPRIETARY_BACKEND_NAME',
    "Django")


class KeepRequestCore(OAuthLibCore):
    """
    Subclass of OAuthLibCore used only for the sake of keeping the django
    request object by placing it in the headers.
    This is a hack and we need a better solution for this.
    """
    def _extract_params(self, request):
        uri, http_method, body, headers = super(
            KeepRequestCore, self)._extract_params(request)
        headers["Django-request-object"] = request
        return uri, http_method, body, headers


class DjangoOAuth2(BaseOAuth2):
    """Default OAuth2 authentication backend used by this package"""
    name = PROPRIETARY_BACKEND_NAME
    AUTHORIZATION_URL = reverse_lazy('auth:authorize')
    ACCESS_TOKEN_URL = reverse_lazy('auth:token')
