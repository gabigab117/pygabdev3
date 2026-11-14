from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField

from .forms import TURNSTILE_FIELD_NAME, TurnstileFormBuilder


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class FormPage(AbstractEmailForm):
    form_builder = TurnstileFormBuilder
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    def process_form_submission(self, form):
        # The token serves once, to Cloudflare: it belongs neither in the stored
        # submission nor in the email.
        form.cleaned_data.pop(TURNSTILE_FIELD_NAME)
        return super().process_form_submission(form)
