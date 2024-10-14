from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from wagtail.models import Page

from core.models import GenericPage


class HomePage(GenericPage):
    body = RichTextField(blank=True)

    content_panels = GenericPage.content_panels + [
        FieldPanel('header'),
        FieldPanel('body')
    ]
