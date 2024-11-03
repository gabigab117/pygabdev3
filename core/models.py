from wagtail.fields import RichTextField

from wagtail.models import Page


class GenericPage(Page):
    header = RichTextField(blank=True)

    class Meta:
        abstract = True
