# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls


from users.transactions import change_email, cancel_account

admin.site.site_header = 'Warp'
admin.autodiscover()

urlpatterns = [
    # Django Admin


    # Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin-tools/', include('admin_tools.urls')),

    # Bloging
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),


    # User management
    # url(r'^$', TemplateView.as_view(template_name='landing.html'), name="home"),
    url(r'^offline/$', TemplateView.as_view(template_name='offline.html')),


    # Transactions
    url(r'^account/change-email/(?P<token>.*)/$', change_email, name="change-email"),
    url(r'^account/cancel-account/(?P<token>.*)/$', cancel_account, name="cancel-account"),


    url(r'', include('blog.urls', namespace='blog')),
    url(r'', include(wagtail_urls)),

]


def mediafiles_urlpatterns(prefix):
    """
    Method for serve media files with runserver.
    """
    import re
    from django.views.static import serve

    return [
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
            {'document_root': settings.MEDIA_ROOT})
    ]

if settings.DEBUG:

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic.base import RedirectView

    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")

    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(
            url=settings.STATIC_URL + 'favicon.ico', permanent=True)
            )
    ]

    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]

    # Test error pages
    urlpatterns += [
        url(r'^error/400/$', TemplateView.as_view(template_name='errors/400.html')),
        url(r'^error/403/$', TemplateView.as_view(template_name='errors/403.html')),
        url(r'^error/404/$', TemplateView.as_view(template_name='errors/404.html')),
        url(r'^error/500/$', TemplateView.as_view(template_name='errors/500.html')),
    ]

    # Test mail templates
    urlpatterns += [
        url(r'^mail/account-activation/$',
            TemplateView.as_view(template_name='emails/account_activation-body.html')),

        url(r'^mail/welcome/$',
            TemplateView.as_view(template_name='emails/account_welcome-body.html')),

        url(r'^mail/reset-password/$',
            TemplateView.as_view(template_name='emails/reset_password-body.html')),

        url(r'^mail/reset-password-success/$',
            TemplateView.as_view(template_name='emails/reset_password_success-body.html')),

        url(r'^mail/change-email/$',
            TemplateView.as_view(template_name='emails/change_email-body.html')),

        url(r'^mail/change-email-success/$',
            TemplateView.as_view(template_name='emails/change_email_success-body.html')),

        url(r'^mail/cancel-account/$',
            TemplateView.as_view(template_name='emails/cancel_account-body.html')),

    ]

    try:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    except Exception as e:
        pass
else:
    pass
    handler400 = TemplateView.as_view(template_name="errors/400.html")
    handler403 = TemplateView.as_view(template_name="errors/403.html")
    handler404 = TemplateView.as_view(template_name="errors/404.html")
    handler500 = TemplateView.as_view(template_name="errors/500.html")