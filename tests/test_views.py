import datetime

import pytest
from django.test import Client
from django.urls import reverse

from customers.models import Service


@pytest.mark.django_db
def test_dashboard_view(client: Client, admin):
    client.force_login(admin)
    response = client.get(reverse("customers:dashboard"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_projects_view(client: Client, admin):
    client.force_login(admin)
    response = client.get(reverse("customers:projects"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_projects_view_filtered_by_customer(
    client: Client, admin, project_1, project_3, customer_1
):
    """
    Scenario: Filter the projects list by customer
        Given I am an authenticated administrator
            And projects exist for several customers
        When I request the projects list filtered on one customer
        Then only that customer's projects are returned
    """
    client.force_login(admin)
    response = client.get(reverse("customers:projects"), {"customer": customer_1.id})
    assert response.status_code == 200
    projects = list(response.context["object_list"])
    assert project_1 in projects
    assert project_3 not in projects


@pytest.mark.django_db
def test_projects_filter_non_numeric_value(client: Client, admin, project_1, project_3):
    """
    Scenario: Filter with a non-numeric customer value
        Given I am an authenticated administrator
            And projects exist for several customers
        When I request the projects list with a non-numeric customer param
        Then all projects are returned (filter is ignored)
    """
    client.force_login(admin)
    response = client.get(reverse("customers:projects"), {"customer": "abc"})
    assert response.status_code == 200
    projects = list(response.context["object_list"])
    assert project_1 in projects
    assert project_3 in projects


@pytest.mark.django_db
def test_projects_filter_nonexistent_customer_id(
    client: Client, admin, project_1, project_3
):
    """
    Scenario: Filter with a numeric but non-existent customer id
        Given I am an authenticated administrator
            And projects exist for several customers
        When I request the projects list with an id that matches no customer
        Then all projects are returned (filter is ignored)
    """
    client.force_login(admin)
    response = client.get(reverse("customers:projects"), {"customer": "99999"})
    assert response.status_code == 200
    projects = list(response.context["object_list"])
    assert project_1 in projects
    assert project_3 in projects


@pytest.mark.django_db
def test_create_service_view(client: Client, project_1, admin, today):
    """
    Scenario: Create a new service
        Given I am an authenticated administrator
            And I have a project
        When I submit a new service form with time data
        Then the service should be created successfully
            And I should be redirected to the appropriate page
    """
    client.force_login(admin)
    data = {
        "date": today,
        "time_spent": 0.25,
    }
    response = client.post(
        reverse("customers:add-service", kwargs={"pk": project_1.pk}), data=data
    )

    assert Service.objects.all().count() == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_service_view(client: Client, service_1: Service, admin, today):
    """
    Scenario: Update an existing service
        Given I am an authenticated administrator
            And I have an existing service
        When I submit updated service time data
        Then the service should be updated successfully
            And the time spent should be modified
            And I should be redirected to the appropriate page
    """
    client.force_login(admin)
    data = {
        "date": today - datetime.timedelta(days=-1),
        "time_spent": 0.21,
    }
    response = client.post(
        reverse("customers:update-service", kwargs={"pk": service_1.pk}), data=data
    )
    service_1.refresh_from_db()
    assert service_1.time_spent == 0.21
    assert response.status_code == 302


@pytest.mark.django_db
def test_mark_service_as_billed(client: Client, admin, service_1: Service, today):
    """
    Scenario: Mark a service as billed once it is invoiced on facture.net
        Given I am an authenticated administrator
            And an unbilled service exists
        When I submit the service form with "Facturé" checked
        Then the service is billed
    """
    client.force_login(admin)
    data = {"date": today, "time_spent": service_1.time_spent, "billed": "on"}

    response = client.post(
        reverse("customers:update-service", kwargs={"pk": service_1.pk}), data=data
    )

    service_1.refresh_from_db()
    assert response.status_code == 302
    assert service_1.billed


@pytest.mark.django_db
def test_service_of_archived_invoice_stays_billed(
    client: Client, admin, invoice_1_with_services, service_1: Service, today
):
    """
    Scenario: A service of an archived invoice cannot be unbilled
        Given I am an authenticated administrator
            And a service belongs to an archived invoice
        When I submit the service form with "Facturé" unchecked
        Then the form is refused with an error on "Facturé"
            And the service is still billed
    """
    client.force_login(admin)
    data = {"date": today, "time_spent": service_1.time_spent}

    response = client.post(
        reverse("customers:update-service", kwargs={"pk": service_1.pk}), data=data
    )

    service_1.refresh_from_db()
    assert response.status_code == 200
    assert "billed" in response.context["form"].errors
    assert service_1.billed


@pytest.mark.django_db
def test_search_view(client: Client, admin, customer_1):
    """
    Scenario: Open the back-office search page
        Given I am an authenticated administrator
            And a customer exists
        When I open the search page, before typing anything
        Then the page is displayed
            And no customer, project or service is listed yet
    """
    client.force_login(admin)

    response = client.get(reverse("customers:search"))

    assert response.status_code == 200
    assert customer_1.name not in response.content.decode()
    assert "Aucun client ne correspond" in response.content.decode()
