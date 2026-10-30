import pytest
from django.test import Client
from django.urls import reverse

from customers.models import Invoice


@pytest.mark.django_db
def test_invoice_admin_shows_archived_invoices(client: Client, admin, invoice_1):
    """
    Scenario: Consult the archived invoices in the Django admin
        Given I am an authenticated administrator
            And an invoice made before facture.net exists
        When I open the invoices list, then the invoice, in the Django admin
        Then the invoice is listed
            And its page is displayed
    """
    client.force_login(admin)

    changelist = client.get(reverse("admin:customers_invoice_changelist"))
    change = client.get(reverse("admin:customers_invoice_change", args=[invoice_1.pk]))

    assert changelist.status_code == 200
    assert invoice_1 in changelist.context["cl"].result_list
    assert change.status_code == 200


@pytest.mark.django_db
def test_invoice_admin_is_read_only(client: Client, admin, invoice_1):
    """
    Scenario: The archived invoices can no longer be added, changed or deleted
        Given I am an authenticated administrator
            And an archived invoice exists
        When I try to add, change or delete an invoice in the Django admin
        Then each attempt is refused
            And the invoice is unchanged
    """
    client.force_login(admin)

    add = client.get(reverse("admin:customers_invoice_add"))
    change = client.post(
        reverse("admin:customers_invoice_change", args=[invoice_1.pk]),
        data={
            "customer": invoice_1.customer_id,
            "number": 99,
            "issue_date": "2024-01-01",
            "delivery_date": "2024-01-02",
            "due_date": "2024-02-01",
        },
    )
    delete = client.post(
        reverse("admin:customers_invoice_delete", args=[invoice_1.pk]),
        data={"post": "yes"},
    )

    assert add.status_code == 403
    assert change.status_code == 403
    assert delete.status_code == 403
    assert Invoice.objects.filter(pk=invoice_1.pk, number=1).exists()
