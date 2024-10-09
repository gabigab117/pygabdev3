from lib2to3.fixes.fix_input import context

from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock

from core.models import GenericPage
from django.db import models


class BlogIndexPage(GenericPage):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request,*args, **kwargs)
        blogpages = BlogPage.objects.child_of(self).live().order_by("-date")
        context["blogpages"] = blogpages
        return context


class BlogPage(GenericPage):
    date = models.DateField(verbose_name="Date de publication")
    body = StreamField([
        ("paragraphe", blocks.RichTextBlock()),
        ("code", CodeBlock()),
    ], use_json_field=True)

    search_fields = GenericPage.search_fields + [
        index.SearchField("header"),
        index.SearchField("body")
    ]

    content_panels = GenericPage.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
        ]
