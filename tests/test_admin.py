import pytest
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.test import Client
from django.urls import reverse

from customers.models import Invoice

from .factories import ServiceFactory


def mark_as_billed(client, services, confirm=False):
    """Run the bulk action of the services list on these services."""
    data = {"action": "mark_as_billed", ACTION_CHECKBOX_NAME: [s.pk for s in services]}
    if confirm:
        data["post"] = "yes"
    return client.post(reverse("admin:customers_service_changelist"), data)


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


@pytest.mark.django_db
def test_invoice_admin_has_no_link_to_a_removed_page(client: Client, admin, invoice_1):
    """
    Scenario: An archived invoice no longer links to the back office
        Given I am an authenticated administrator
            And an archived invoice exists
        When I open the invoice in the Django admin
        Then no "Voir sur le site" link is offered
            And the address of that link answers 404, not a server error
    """
    client.force_login(admin)
    content_type = ContentType.objects.get_for_model(Invoice)

    change = client.get(reverse("admin:customers_invoice_change", args=[invoice_1.pk]))
    view_on_site = client.get(
        reverse("admin:view_on_site", args=[content_type.pk, invoice_1.pk])
    )

    assert not change.context["has_absolute_url"]
    assert view_on_site.status_code == 404


@pytest.mark.django_db
def test_service_admin_filters_by_customer(
    client: Client, admin, service_1, service_3, service_4
):
    """
    Scenario: Filter the services of the Django admin by customer
        Given I am an authenticated administrator
            And services exist for several customers
        When I filter the services list on one customer
        Then only that customer's services are listed
    """
    client.force_login(admin)

    response = client.get(
        reverse("admin:customers_service_changelist"),
        {"project__customer__id__exact": service_1.project.customer_id},
    )

    assert response.status_code == 200
    assert set(response.context["cl"].result_list) == {service_1, service_3}


@pytest.mark.django_db
def test_mark_as_billed_asks_for_confirmation(
    client: Client, admin, service_1, service_2
):
    """
    Scenario: The bulk action shows the amount before marking anything
        Given I am an authenticated administrator
            And two unbilled services exist
        When I run "Marquer comme facturés" on them
        Then a confirmation page shows their total amount and hours
            And no service is billed yet
    """
    client.force_login(admin)

    response = mark_as_billed(client, [service_1, service_2])

    service_1.refresh_from_db()
    service_2.refresh_from_db()
    assert response.status_code == 200
    assert response.context["total"] == 350
    assert response.context["hours"] == 3.5
    assert "350,00 €" in response.content.decode()
    assert not service_1.billed
    assert not service_2.billed


@pytest.mark.django_db
def test_mark_as_billed_once_confirmed(
    client: Client, admin, service_1, service_2, service_3
):
    """
    Scenario: Confirming marks the selected services as billed
        Given I am an authenticated administrator
            And three unbilled services exist
        When I confirm "Marquer comme facturés" on two of them
        Then I am sent back to the services list
            And those two services are billed
            And the third one is not
    """
    client.force_login(admin)

    response = mark_as_billed(client, [service_1, service_2], confirm=True)

    for service in (service_1, service_2, service_3):
        service.refresh_from_db()
    assert response.status_code == 302
    assert service_1.billed
    assert service_2.billed
    assert not service_3.billed


@pytest.mark.django_db
def test_mark_as_billed_ignores_billed_services(
    client: Client, admin, invoice_1_with_services, service_1, service_3
):
    """
    Scenario: Services already billed are left out of the amount
        Given I am an authenticated administrator
            And a service billed on an archived invoice
            And an unbilled service
        When I run "Marquer comme facturés" on both
        Then the confirmation page lists only the unbilled service
            And its amount only
            And says one service is left out
    """
    client.force_login(admin)

    response = mark_as_billed(client, [service_1, service_3])

    assert list(response.context["services"]) == [service_3]
    assert response.context["total"] == 30
    assert response.context["ignored"] == 1


@pytest.mark.django_db
def test_mark_as_billed_with_nothing_to_bill(
    client: Client, admin, invoice_1_with_services, service_1
):
    """
    Scenario: A selection with nothing left to bill
        Given I am an authenticated administrator
            And a service billed on an archived invoice
        When I run "Marquer comme facturés" on it
        Then I am sent back to the services list with a warning
    """
    client.force_login(admin)

    response = mark_as_billed(client, [service_1])

    assert response.status_code == 302
    assert "Aucun service à facturer dans la sélection." in [
        str(message) for message in get_messages(response.wsgi_request)
    ]


@pytest.mark.django_db
def test_mark_as_billed_needs_the_change_permission(
    client: Client, service_viewer, service_1
):
    """
    Scenario: A staff account that can only view the services cannot bill them
        Given I am a staff account allowed to view the services, not to change them
        When I confirm "Marquer comme facturés" on a service
        Then the service is still unbilled
    """
    client.force_login(service_viewer)

    mark_as_billed(client, [service_1], confirm=True)

    service_1.refresh_from_db()
    assert not service_1.billed


@pytest.mark.django_db
def test_mark_as_billed_rounds_the_total_hours(client: Client, admin, project_1):
    """
    Scenario: The total hours stay readable whatever the decimals
        Given I am an authenticated administrator
            And two unbilled services of 0.1 and 0.2 hours
        When I run "Marquer comme facturés" on them
        Then the confirmation page shows 0,30 h in total
    """
    client.force_login(admin)
    services = [
        ServiceFactory(project=project_1, date="2024-03-01", time_spent=0.1),
        ServiceFactory(project=project_1, date="2024-03-02", time_spent=0.2),
    ]

    response = mark_as_billed(client, services)

    assert "<th>0,30 h</th>" in response.content.decode()
