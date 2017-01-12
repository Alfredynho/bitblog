# -*- coding: utf-8 -*-
import datetime

from django.conf import settings

from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, \
    StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.fields import ParentalKey

from apps.blog.blocks import CodeBlock, MarkDownBlock, RSTBlock
from .routes import BlogRoutes
from .managers import TagManager, CategoryManager


class BlogPage(BlogRoutes, Page):

    description = models.CharField(
        verbose_name=_('Description'),
        max_length=255,
        blank=True,
        help_text=_("The blog description that will appear under the title."),
    )

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Header image'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    display_comments = models.BooleanField(
        default=False,
        verbose_name=_('Display comments'),
    )

    display_categories = models.BooleanField(
        default=True,
        verbose_name=_('Display categories'),
    )

    display_tags = models.BooleanField(
        default=True,
        verbose_name=_('Display tags'),
    )

    display_popular_entries = models.BooleanField(
        default=True,
        verbose_name=_('Display popular entries'),
    )

    display_last_entries = models.BooleanField(
        default=True,
        verbose_name=_('Display last entries'),
    )

    display_archive = models.BooleanField(
        default=True,
        verbose_name=_('Display archive'),
    )

    disqus_api_secret = models.TextField(
        blank=True
    )

    disqus_shortname = models.CharField(
        max_length=128,
        blank=True,
    )

    num_entries_page = models.IntegerField(
        default=5,
        verbose_name=_('Entries per page'),
    )

    num_last_entries = models.IntegerField(
        default=3,
        verbose_name=_('Last entries limit'),
    )

    num_popular_entries = models.IntegerField(
        default=3,
        verbose_name=_('Popular entries limit'),
    )

    num_tags_entry_header = models.IntegerField(
        default=5,
        verbose_name=_('Tags limit entry header'),
    )

    content_panels = Page.content_panels + [

        FieldPanel('description', classname="full"),
        ImageChooserPanel('header_image'),

        MultiFieldPanel([
            InlinePanel('blog_projects', label=_("Projects")),
            InlinePanel('blog_speeches', label=_("Speeches")),
        ], heading=_("Portfolio")),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('owner', classname="full"),
        MultiFieldPanel([
            FieldPanel('display_categories'),
            FieldPanel('display_tags'),
            FieldPanel('display_popular_entries'),
            FieldPanel('display_last_entries'),
            FieldPanel('display_archive'),
        ], heading=_("Widgets")),
        MultiFieldPanel([
            FieldPanel('num_entries_page'),
            FieldPanel('num_last_entries'),
            FieldPanel('num_popular_entries'),
            FieldPanel('num_tags_entry_header'),
        ], heading=_("Parameters")),
        MultiFieldPanel([
            FieldPanel('display_comments'),
            FieldPanel('disqus_api_secret'),
            FieldPanel('disqus_shortname'),
        ], heading=_("Comments")),
    ]

    subpage_types = ['blog.EntryPage']

    def get_entries(self):
        field_name = 'owner__%s' % getattr(settings, 'PUPUT_USERNAME_FIELD', 'username')
        return EntryPage.objects.descendant_of(self).live().order_by('-date').select_related('owner')


    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['entries'] = self.entries
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        return context

    class Meta:
        verbose_name = _('Blog')


@register_snippet
class Category(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_('Category name'),
    )

    icon = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Icon'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    slug = models.SlugField(
        unique=True,
        max_length=80,
    )

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True, related_name="children",
        verbose_name=_('Parent category'),
    )

    description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Description'),
    )

    objects = CategoryManager()

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('slug'),
                ImageChooserPanel('icon'),
                SnippetChooserPanel('parent'),
                FieldPanel('description', classname="full"),
            ],
            heading=_("Category"),
        )
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent and parent.parent == self:
                raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


@register_snippet
class Project(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_('Project name'),
    )

    link = models.URLField(
        unique=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Description'),
    )

    thumb = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Thumb'),
        help_text=_("Small image to previsualization 350 x 350"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Image'),
        help_text=_("Full visualization image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('description', classname="full"),
                FieldPanel('link'),
            ],
            heading=_("Info"),
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('thumb'),
                ImageChooserPanel('image'),
            ],
            heading=_("Images"),
        )
    ]


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


@register_snippet
class Speech(models.Model):
    title = models.CharField(
        max_length=140,
        unique=True,
        verbose_name=_('Speech title'),
    )

    community = models.CharField(
        max_length=140,
        unique=True,
        verbose_name=_('Community'),
    )

    link = models.URLField(
        verbose_name=_('Link to slides'),
        unique=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Description'),
    )

    thumb = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Thumb'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title', classname="title"),
                FieldPanel('description', classname="full"),
                FieldPanel('community'),
                FieldPanel('link'),
            ],
            heading=_("Info"),
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('thumb'),
                ImageChooserPanel('image'),
            ],
            heading=_("Images"),
        )
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Speech")
        verbose_name_plural = _("Speeches")


class CategoryEntryPage(models.Model):
    category = models.ForeignKey(
        'Category',
        related_name="+",
        verbose_name=_('Category'),
    )

    page = ParentalKey(
        'EntryPage',
        related_name='entry_categories',
    )

    panels = [
        FieldPanel('category')
    ]


class ProjectBlogPage(models.Model):
    project = models.ForeignKey(
        'Project',
        related_name="+",
        verbose_name=_('Project'),
    )

    page = ParentalKey(
        'BlogPage',
        related_name='blog_projects',
    )

    panels = [
        SnippetChooserPanel('project')
    ]


class SpeechBlogPage(models.Model):
    speech = models.ForeignKey(
        'Speech',
        related_name="+",
        verbose_name=_('Speech'),
    )

    page = ParentalKey(
        'BlogPage',
        related_name='blog_speeches',
    )

    panels = [
        SnippetChooserPanel('speech')
    ]


class TagEntryPage(TaggedItemBase):
    content_object = ParentalKey(
        'EntryPage',
        related_name='entry_tags',
    )


@register_snippet
class Tag(TaggitTag):
    objects = TagManager()

    class Meta:
        proxy = True


class EntryPageRelated(models.Model):
    entrypage_from = ParentalKey(
        'EntryPage',
        verbose_name=_("Entry"),
        related_name='related_entrypage_from',
    )

    entrypage_to = ParentalKey(
        'EntryPage', verbose_name=_("Entry"),
        related_name='related_entrypage_to',
    )


class EntryPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(
            classname="full title",
            template="blog/blocks/heading.html",
            label=_("Titulo"),
        )),
        ('paragraph', blocks.RichTextBlock(
            label=_("Párrafo"),
            # icon='pilcrow',
        )),
        ('image', ImageChooserBlock(
            label=_("Imagen"),
            template="blog/blocks/image.html",
        )),
        ('code', CodeBlock(
            label=_("Código"),
        )),
        ('table', TableBlock(
            label=_("Tabla"),
        )),
    ])

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

    author_avatar = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('avatar'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    author_phrase = RichTextField(
        verbose_name=_('phrase'),
        null=True,
        blank=True,
    )

    num_comments = models.IntegerField(
        default=0,
        editable=False,
    )

    # Search
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('excerpt'),
        index.FilterField('page_ptr_id')
    ]

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            ImageChooserPanel('header_image'),
            FieldPanel('show_header', classname="full"),
            StreamFieldPanel('body'),
            FieldPanel('excerpt', classname="full"),
        ], heading=_("Content")),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('entry_categories', label=_("Categories")),
            InlinePanel('related_entrypage_from', label=_("Related Entries")),
        ], heading=_("Metadata")),

    ]

    promote_panels = Page.promote_panels

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
        MultiFieldPanel(
            [
                FieldPanel('owner'),
                ImageChooserPanel('author_avatar'),
                FieldPanel('author_phrase'),
            ], heading=_("Author")
        ),

    ]

    # Parent and child settings
    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    @property
    def blog_page(self):
        return BlogPage.objects.ancestor_of(self).first()

    @property
    def related(self):
        return [related.entrypage_to for related in self.related_entrypage_from.all()]

    @property
    def has_related(self):
        return self.related_entrypage_from.count() > 0

    def get_context(self, request, *args, **kwargs):
        context = super(EntryPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
EntryPage._meta.get_field('owner').editable = True
