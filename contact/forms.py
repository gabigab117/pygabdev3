"""
Cloudflare Turnstile, the anti-robot check of the contact form.

Neither Django nor Wagtail covers Turnstile, and the two packages on PyPI were ruled
out: wagtail-turnstile calls Cloudflare without a timeout and makes the check a field
type to add in the admin; django-turnstile turns a network error into a server error
and silently falls back to the test keys, which let everything through.
"""

import logging

import requests
from django import forms
from django.conf import settings
from wagtail.contrib.forms.forms import FormBuilder

logger = logging.getLogger(__name__)

SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
TURNSTILE_FIELD_NAME = "turnstile"
# Cloudflare's error codes that come from the visitor's token. Any other one means
# that the site itself fails the check, and then every prospect is refused.
VISITOR_ERROR_CODES = {"invalid-input-response", "timeout-or-duplicate"}


class TurnstileWidget(forms.Widget):
    template_name = "contact/widgets/turnstile.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["site_key"] = settings.TURNSTILE_SITE_KEY
        return context

    def value_from_datadict(self, data, files, name):
        # The widget puts its token in a hidden input that it names itself.
        return data.get("cf-turnstile-response")


class TurnstileField(forms.Field):
    widget = TurnstileWidget
    default_error_messages = {
        "required": "Attendez la fin de la vérification anti-robot, puis renvoyez le formulaire.",
        "invalid": "La vérification anti-robot n'a pas abouti. Réessayez dans un instant.",
    }

    def validate(self, value):
        super().validate(value)
        try:
            answer = requests.post(
                SITEVERIFY_URL,
                data={"secret": settings.TURNSTILE_SECRET_KEY, "response": value},
                timeout=5,
            ).json()
        except requests.RequestException as error:
            logger.warning("Turnstile siteverify unreachable: %s", type(error).__name__)
            answer = {}
        if answer.get("success") is True:
            return
        error_codes = answer.get("error-codes", [])
        if set(error_codes) - VISITOR_ERROR_CODES:
            logger.warning("Turnstile siteverify refused the site: %s", error_codes)
        raise forms.ValidationError(self.error_messages["invalid"], code="invalid")


class TurnstileFormBuilder(FormBuilder):
    """Adds the anti-robot check to the fields declared in the Wagtail admin."""

    @property
    def formfields(self):
        fields = super().formfields
        fields[TURNSTILE_FIELD_NAME] = TurnstileField(label="")
        return fields
