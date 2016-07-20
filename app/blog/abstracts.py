import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.wagtailcore.fields import RichTextField


class EntryAbstract(models.Model):
    body = RichTextField(
        verbose_name=_('body'),
    )

    tags = ClusterTaggableManager(
        through='blog.TagEntryPage',
        blank=True,
    )

    date = models.DateTimeField(
        verbose_name=_("Post date"),
        default=datetime.datetime.today,
    )

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Header image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    show_header = models.BooleanField(
        verbose_name=_('Show header'),
        help_text=_('Show header image in main list'),
        default=False,
    )

    categories = models.ManyToManyField(
        'blog.Category',
        through='blog.CategoryEntryPage',
        blank=True,
    )

    excerpt = RichTextField(
        verbose_name=_('excerpt'),
        blank=True,
        help_text=_("Entry excerpt to be displayed on entries list. "
                        "If this field is not filled, a truncate version of body text will be used."),
    )

    num_comments = models.IntegerField(
        default=0,
        editable=False,
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            ImageChooserPanel('header_image'),
            FieldPanel('show_header', classname="full"),
            FieldPanel('body', classname="full"),
            FieldPanel('excerpt', classname="full"),
        ], heading=_("Content")),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('entry_categories', label=_("Categories")),
            InlinePanel('related_entrypage_from', label=_("Related Entries")),
            InlinePanel('entry_categories', label=_("Categories")),

        ], heading=_("Metadata")),
    ]

    class Meta:
        abstract = True
