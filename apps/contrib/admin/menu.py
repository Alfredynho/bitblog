# -*- encoding:utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu as MenuBase


class Menu(MenuBase):
    """
    Custom Menu for code admin site.
    """
    def __init__(self, **kwargs):
        MenuBase.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),

            items.AppList(
                _('TODOS'),
                exclude=('django.contrib.*',)
            ),

            items.ModelList(
                title=_('Autenticación'),
                models=[
                    'rest_framework.authtoken.*',
                    'oauth2_provider.*',
                    'auths.models.*',
                    'apps.credentials.models.PlatformApp',
                ]
            ),

        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(Menu, self).init_with_context(context)
