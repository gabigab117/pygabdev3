import logging

import pytest
import requests
from django.conf import settings
from wagtail.contrib.forms.models import FormSubmission

FORM_DATA = {
    "email": "prospect@example.org",
    "message": "Bonjour, un projet à vous proposer.",
    "cf-turnstile-response": "token-from-the-widget",
}


@pytest.mark.django_db
def test_contact_page_shows_the_turnstile_widget(client, contact_page):
    """
    Scenario: Show the anti-robot check on the contact page
        Given the contact page
        When a visitor opens it
        Then the Turnstile widget is shown with the site key
    """
    response = client.get(contact_page.url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "challenges.cloudflare.com/turnstile/v0/api.js" in content
    assert f'data-sitekey="{settings.TURNSTILE_SITE_KEY}"' in content


@pytest.mark.django_db
def test_contact_form_sent_when_cloudflare_accepts_the_token(
    client, contact_page, siteverify, mailoutbox
):
    """
    Scenario: Send the contact form once the anti-robot check passes
        Given the contact page
        When a visitor sends the form with a token that Cloudflare accepts
        Then the thank-you page is shown
            And the message is emailed and stored, without the token
    """
    response = client.post(contact_page.url, FORM_DATA)

    assert "Message bien reçu" in response.content.decode()
    assert siteverify.call_args.kwargs["data"] == {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": "token-from-the-widget",
    }
    assert siteverify.call_args.kwargs["timeout"] == 5
    assert len(mailoutbox) == 1
    assert "token-from-the-widget" not in mailoutbox[0].body
    assert FormSubmission.objects.get(page=contact_page).form_data == {
        "email": "prospect@example.org",
        "message": "Bonjour, un projet à vous proposer.",
    }


@pytest.mark.django_db
def test_contact_form_refused_when_cloudflare_rejects_the_token(
    client, contact_page, siteverify, mailoutbox, caplog
):
    """
    Scenario: Refuse the contact form when Cloudflare rejects the token
        Given the contact page
        When a visitor sends the form with a token that Cloudflare rejects
        Then the form is shown again with an error
            And no message is emailed or stored
            And no warning is logged, since the token is the visitor's
    """
    siteverify.return_value.json.return_value = {
        "success": False,
        "error-codes": ["invalid-input-response"],
    }

    response = client.post(contact_page.url, FORM_DATA)

    assert "Réessayez dans un instant" in response.content.decode()
    assert mailoutbox == []
    assert not FormSubmission.objects.exists()
    assert not [record for record in caplog.records if record.name == "contact.forms"]


@pytest.mark.django_db
def test_contact_form_refused_without_a_token(
    client, contact_page, siteverify, mailoutbox
):
    """
    Scenario: Refuse the contact form sent before the anti-robot check ends
        Given the contact page
        When a visitor sends the form while the Turnstile token is still empty
        Then the form is shown again with an error
            And Cloudflare is not called
            And no message is emailed or stored
    """
    data = {**FORM_DATA, "cf-turnstile-response": ""}

    response = client.post(contact_page.url, data)

    assert "Attendez la fin de la vérification anti-robot" in response.content.decode()
    siteverify.assert_not_called()
    assert mailoutbox == []
    assert not FormSubmission.objects.exists()


@pytest.mark.django_db
def test_contact_form_refused_when_cloudflare_is_unreachable(
    client, contact_page, siteverify, mailoutbox, caplog
):
    """
    Scenario: Refuse the contact form when Cloudflare cannot be reached
        Given the contact page
            And Cloudflare does not answer
        When a visitor sends the form
        Then the form is shown again with an error, not a server error
            And no message is emailed or stored
            And a warning is logged
    """
    siteverify.side_effect = requests.ConnectionError

    response = client.post(contact_page.url, FORM_DATA)

    assert response.status_code == 200
    assert "Réessayez dans un instant" in response.content.decode()
    assert mailoutbox == []
    assert not FormSubmission.objects.exists()
    assert [
        record.levelno for record in caplog.records if record.name == "contact.forms"
    ] == [logging.WARNING]


@pytest.mark.django_db
def test_site_refused_by_cloudflare_is_logged(client, contact_page, siteverify, caplog):
    """
    Scenario: Leave a trace when Cloudflare refuses the site itself
        Given the contact page
            And Cloudflare rejects the secret key of the site
        When a visitor sends the form
        Then the form is refused
            And a warning names Cloudflare's error code
            And it shows neither the secret key nor the token
    """
    siteverify.return_value.json.return_value = {
        "success": False,
        "error-codes": ["invalid-input-secret"],
    }

    response = client.post(contact_page.url, FORM_DATA)

    assert "Réessayez dans un instant" in response.content.decode()
    assert "invalid-input-secret" in caplog.text
    assert settings.TURNSTILE_SECRET_KEY not in caplog.text
    assert "token-from-the-widget" not in caplog.text
