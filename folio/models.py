from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.models import Image
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock

from core.models import GenericPage


class FolioIndexPage(GenericPage):
    content_panels = GenericPage.content_panels + [
        FieldPanel("header"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        foliopages = FolioPage.objects.child_of(self).live().order_by("-date")
        context["foliopages"] = foliopages
        return context


class FolioPage(GenericPage):
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
    youtube = models.URLField(verbose_name="Lien Youtube", blank=True)
    github = models.URLField(verbose_name="Lien GitHub", blank=True)
    production = models.URLField(verbose_name="Lien du Projet", blank=True)

    search_fields = GenericPage.search_fields + [
        index.SearchField("header"),
        index.SearchField("body"),
    ]

    content_panels = GenericPage.content_panels + [
        MultiFieldPanel(
            [FieldPanel("header"), FieldPanel("date"), FieldPanel("main_image")],
            heading="En-tête",
        ),
        MultiFieldPanel([FieldPanel("body")], heading="Corps"),
        MultiFieldPanel(
            [FieldPanel("youtube"), FieldPanel("github"), FieldPanel("production")],
            heading="Liens",
        ),
    ]
