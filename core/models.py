from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class GenericPage(Page):
    header = RichTextField(blank=True)

    class Meta:
        abstract = True


class LegalPage(GenericPage):
    body = RichTextField()

    content_panels = GenericPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
    ]
