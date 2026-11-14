import re

import pytest

# The hosts the public site loads scripts from: htmx (unpkg), Bootstrap (jsDelivr),
# Simple Analytics, which sets no cookie, and Turnstile. A tracker that sets
# cookies needs a consent mechanism first (CLAUDE.md, Architecture).
THIRD_PARTY_HOSTS = {
    "unpkg.com",
    "cdn.jsdelivr.net",
    "scripts.simpleanalyticscdn.com",
    "challenges.cloudflare.com",
}


@pytest.mark.django_db
def test_public_page_loads_no_cookie_banner_nor_tracker(client, contact_page):
    """
    Scenario: Visit the public site, which sets no tracking cookie
        Given a page of the public site
        When a visitor opens it
        Then no cookie banner is shown
            And scripts and frames come only from the expected hosts
            And the only cookie set is the CSRF cookie of the form
    """
    response = client.get(contact_page.url)

    content = response.content.decode()
    assert "cookie-consent" not in content
    hosts = re.findall(r'<(?:script|iframe)[^>]*\ssrc="https?://([^/"]+)', content)
    assert set(hosts) == THIRD_PARTY_HOSTS
    assert set(response.cookies) <= {"csrftoken"}


@pytest.mark.django_db
def test_cookies_page_is_gone(client):
    """
    Scenario: Open the former cookies page
        Given the site has no cookie banner anymore
        When a visitor opens /cookies/
        Then the page is not found
    """
    assert client.get("/cookies/").status_code == 404
