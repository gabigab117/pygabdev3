from project.settings import dev


def test_development_prints_emails_to_the_console():
    """
    Scenario: Send an email in development
        Given the development settings
        When the site sends an email, from the contact form for instance
        Then the email is printed in the console of runserver, never sent
    """
    assert dev.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend"
