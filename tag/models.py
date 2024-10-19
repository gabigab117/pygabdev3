from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.models import Page


class TaggedPage(TaggedItemBase):
    content_object = ParentalKey('wagtailcore.Page', related_name="tagged_items", on_delete=models.CASCADE)


class TagIndexPage(Page):

    def get_context(self, request):
        from blog.models import BlogPage
        from folio.models import FolioPage

        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)
        projects = FolioPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context["blogpages"] = blogpages
        context["projects"] = projects
        return context
