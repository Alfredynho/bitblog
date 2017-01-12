# -*- encoding:utf-8 -*-

from apps.credentials.urls.endpoints import urlpatterns as endpoints_urls
from apps.credentials.urls.views import urlpatterns as views_urls

urlpatterns = endpoints_urls + views_urls
