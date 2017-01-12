# -*- encoding:utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from apps.contrib.views import LandingView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls


urlpatterns = [

    # Django ADMIN
    url(settings.ADMIN_URL, admin.site.urls),

    # Blog Admin
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^offline/$', TemplateView.as_view(template_name='offline.html')),

    # Blog Pages
    url(r'', include('apps.blog.urls', namespace='blog')),
    url(r'', include(wagtail_urls)),

    # Platform VIEWS and ENDPOINTS
    url(r'', include('apps.users.urls', namespace='users')),
    url(r'', include('apps.credentials.urls', namespace="credentials")),

    # Third parts
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:

    urlpatterns += [
        url(
            regex=r'^test/login/?$',
            view=TemplateView.as_view(template_name='test/login.html')
        ),
    ]

    # Test Email templates
    urlpatterns += [
        url(
            regex=r'^email/base/?$',
            view=TemplateView.as_view(template_name='layouts/base_email.html')
        ),

        url(
            regex=r'^email/web/confirmation/?$',
            view=TemplateView.as_view(template_name='account/email/email_confirmation_message.html')
        ),

        url(
            regex=r'^email/web/signup/?$',
            view=TemplateView.as_view(template_name='account/email/email_confirmation_signup_message.html')
        ),

        url(
            regex=r'^email/web/password-reset/?$',
            view=TemplateView.as_view(template_name='account/email/password_reset_key_message.html')
        ),

        url(
            regex=r'^email/mobile/welcome/?$',
            view=TemplateView.as_view(template_name='credentials/email/account_welcome_message.html')
        ),
    ]

    # Test error pages
    urlpatterns += [
        url(r'^400/$', TemplateView.as_view(template_name='errors/400.html')),
        url(r'^403/$', TemplateView.as_view(template_name='errors/403.html')),
        url(r'^404/$', TemplateView.as_view(template_name='errors/404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='errors/500.html')),
    ]

    urlpatterns += [
        url(r'^error/400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^error/403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^error/404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^error/500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
else:
    handler400 = TemplateView.as_view(template_name="errors/400.html")
    handler403 = TemplateView.as_view(template_name="errors/403.html")
    handler404 = TemplateView.as_view(template_name="errors/404.html")
    handler500 = TemplateView.as_view(template_name="errors/500.html")
