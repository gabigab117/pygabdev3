from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from wagtail.models import Page
from django.db import models


class GenericPage(Page):
    header = RichTextField(blank=True)

    class Meta:
        abstract = True
