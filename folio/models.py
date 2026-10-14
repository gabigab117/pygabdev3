from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.models import Image
from wagtail.models import Orderable
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock

from core.models import GenericPage


class FolioIndexPage(GenericPage):
    content_panels = GenericPage.content_panels + [
        FieldPanel("header"),
    ]
    subpage_types = ["folio.FolioPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        foliopages = (
            FolioPage.objects.child_of(self)
            .live()
            .order_by("-date")
            .prefetch_related("repositories")
        )
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
            [
                InlinePanel("repositories", label="Dépôt GitHub", max_num=4),
                FieldPanel("youtube"),
                FieldPanel("production"),
            ],
            heading="Liens",
        ),
    ]


class FolioRepository(Orderable):
    page = ParentalKey(FolioPage, on_delete=models.CASCADE, related_name="repositories")
    url = models.URLField(verbose_name="Lien GitHub")
    label = models.CharField(
        verbose_name="Libellé",
        max_length=50,
        blank=True,
        help_text="Ex. : Backend, Frontend. Laisser vide pour afficher « GitHub ».",
    )

    panels = [FieldPanel("url"), FieldPanel("label")]

    class Meta(Orderable.Meta):
        verbose_name = "Dépôt GitHub"
        verbose_name_plural = "Dépôts GitHub"
