from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from blog.models import BlogPage
from core.models import GenericPage
from folio.models import FolioPage


class HomePage(GenericPage):
    body = RichTextField(blank=True)

    content_panels = GenericPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        projects = FolioPage.objects.live().order_by("-date")
        context["last_article"] = BlogPage.objects.live().order_by("-date").first()
        context["project"] = projects.first()
        context["recent_projects"] = projects[:8]
        return context
