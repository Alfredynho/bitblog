# -*- encoding:utf-8 -*-

from apps.users.urls.endpoints import urlpatterns as endpoints_urls
from apps.users.urls.views import urlpatterns as views_urls

urlpatterns = endpoints_urls + views_urls
