from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.models import Image
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock

from core.models import GenericPage
from tag.models import BlogTaggedPage


class BlogIndexPage(GenericPage):
    content_panels = GenericPage.content_panels + [
        FieldPanel("header"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blogpages = BlogPage.objects.child_of(self).live().order_by("-date")
        context["blogpages"] = blogpages
        return context


class BlogPage(GenericPage):
    main_image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        verbose_name="Image principale",
        related_name="+",
    )
    date = models.DateField(verbose_name="Date de publication")
    body = StreamField(
        [
            ("paragraphe", blocks.RichTextBlock()),
            ("code", CodeBlock()),
        ],
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through=BlogTaggedPage, blank=True)

    search_fields = GenericPage.search_fields + [
        index.SearchField("header"),
        index.SearchField("body"),
    ]

    content_panels = GenericPage.content_panels + [
        MultiFieldPanel(
            [FieldPanel("header"), FieldPanel("date"), FieldPanel("main_image")],
            heading="En-tête",
        ),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]
