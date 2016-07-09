from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name




class WarpIndexDashboard(Dashboard):
    """
    Custom index dashboard for code.
    """
    columns = 3
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Documentation'), settings.API_DOCS_URL],
                [_('Change password'), reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))


        self.children.append(
            modules.ModelList(
                title=_('Authentication'),
                models=[
                    'rest_framework.authtoken.*',
                    'oauth2_provider.*',
                    'oauth.models.*',
                ]
            )
        )

        self.children.append(
            modules.ModelList(
                title=_('Social Auth'),
                models=[
                    'social.apps.django_app.*',
                ]
            )
        )

        self.children.append(
            modules.ModelList(
                title=_('Administration'),
                models=[
                    'django.contrib.auth.*',
                    'django.contrib.sites.*',
                    'users.models.*',
                ]
            )
        )

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        # self.children.append(modules.Feed(
        #     _('Latest Django News'),
        #     feed_url='http://www.djangoproject.com/rss/weblog/',
        #     limit=5
        # ))

        # append another link list module for "support".
        # self.children.append(modules.LinkList(
        #     _('Support'),
        #     children=[
        #         {
        #             'title': _('Django documentation'),
        #             'url': 'http://docs.djangoproject.com/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django "django-users" mailing list'),
        #             'url': 'http://groups.google.com/group/django-users',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django irc channel'),
        #             'url': 'irc://irc.freenode.net/django',
        #             'external': True,
        #         },
        #     ]
        # ))


class WarpAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for code.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(WarpAppIndexDashboard, self).init_with_context(context)
