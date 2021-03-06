from django.conf import settings
from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from .feeds import BlogPageFeed
from .views import EntryPageServe, EntryPageUpdateCommentsView, PortfolioPage, ContactPage, ContactSuccessPage

urlpatterns = [
    url(
        regex=r'^entry_page/(?P<entry_page_id>\d+)/update_comments/$',
        view=EntryPageUpdateCommentsView.as_view(),
        name='entry_page_update_comments'
    ),
    url(
        regex=r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=EntryPageServe.as_view(),
        name='entry_page_serve_slug'
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=EntryPageServe.as_view(),
        name='entry_page_serve'
    ),
    url(
        regex=r'^(?P<blog_slug>[-\w]+)/feed/$',
        view=BlogPageFeed(),
        name='blog_page_feed_slug'
    ),
    url(
        regex=r'^feed/$',
        view=BlogPageFeed(),
        name='blog_page_feed'
    ),

    url(
        regex=r'^contact/$',
        view=ContactPage.as_view(),
        name='contact_page',
    ),

    url(r'^contact/thanks/$',
        ContactSuccessPage.as_view()
    ),

    url(
        regex=r'^portfolio/$',
        view=PortfolioPage.as_view(),
        name='portfolio_page',
    ),

    url(
        regex=r'^post/$',
        view=TemplateView.as_view(template_name="blog/entry_page.html"),
        name='post_page',
    )
]


# from wagtail.wagtailcore import urls as wagtail_urls
# from wagtail.wagtailadmin import urls as wagtailadmin_urls
# from wagtail.wagtaildocs import urls as wagtaildocs_urls
# from wagtail.wagtailsearch import urls as wagtailsearch_urls
# from wagtail.contrib.wagtailsitemaps.views import sitemap
#
# urlpatterns.extend([
#     url(
#         regex=r'^blog_admin/',
#         view=include(wagtailadmin_urls)
#     ),
#     url(
#         regex=r'',
#         view=include(wagtail_urls)
#     ),
#     url(
#         regex=r'^search/',
#         view=include(wagtailsearch_urls)
#     ),
#     url(
#         regex=r'^documents/',
#         view=include(wagtaildocs_urls)
#     ),
#     url(
#         regex='^sitemap\.xml$',
#         view=sitemap
#     )
#     ])


def get_entry_url(entry, blog_page, root_page):
    """
    Get the entry url given and entry page a blog page instances.
    It will use an url or another depending if blog_page is the root page.
    """
    if root_page == blog_page:
        return reverse('blog:entry_page_serve', kwargs={
            'year': entry.date.strftime('%Y'),
            'month': entry.date.strftime('%m'),
            'day': entry.date.strftime('%d'),
            'slug': entry.slug
        })
    else:
        return reverse('blog:entry_page_serve_slug', kwargs={
            'blog_slug': blog_page.slug,
            'year': entry.date.strftime('%Y'),
            'month': entry.date.strftime('%m'),
            'day': entry.date.strftime('%d'),
            'slug': entry.slug
        })


def get_feeds_url(blog_page, root_page):
    """
    Get the feeds urls a blog page instance.
    It will use an url or another depending if blog_page is the root page.
    """
    if root_page == blog_page:
        return reverse('blog_page_feed')
    else:
        return reverse('blog_page_feed_slug', kwargs={'blog_slug': blog_page.slug})


