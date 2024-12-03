from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.models import Page


class BlogTaggedPage(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogTagIndexPage(Page):
    def get_context(self, request):
        from blog.models import BlogPage

        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag).live()

        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context
