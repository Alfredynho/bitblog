
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class WarpMenu(Menu):
    """
    Custom Menu for code admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),

            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),

            items.ModelList(
                title=_('Authentication'),
                models=[
                    'rest_framework.authtoken.*',
                    'oauth2_provider.*',
                    'oauth.models.*',
                ]
            ),

            items.ModelList(
                title=_('Social Auth'),
                models=[
                    'social.apps.django_app.*',
                ]
            ),

            items.ModelList(
                title=_('Administration'),
                models=[
                    'django.contrib.auth.*',
                    'django.contrib.sites.*',
                    'users.models.*',
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(WarpMenu, self).init_with_context(context)
