from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


from core.models import GenericPage
from blog.models import BlogPage
from folio.models import FolioPage


class HomePage(GenericPage):
    body = RichTextField(blank=True)

    content_panels = GenericPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["last_article"] = BlogPage.objects.live().order_by("-date").first()
        context["project"] = FolioPage.objects.live().order_by("-date").first()
        return context
