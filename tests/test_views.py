import datetime

import pytest
from django.test import Client
from django.urls import reverse

from customers.models import Invoice, Service


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
def test_create_invoice_view(client: Client, admin, customer_1, service_1, today, pdf1):
    """
    Scenario: Create a new invoice
        Given I am an authenticated administrator
            And I have a customer and service
        When I submit a new invoice form with valid data
            And include a service and PDF file
        Then the invoice should be created successfully
            And I should be redirected to the invoices list
    """
    client.force_login(admin)
    data = {
        "customer": customer_1.id,
        "number": 1,
        "issue_date": today,
        "delivery_date": today,
        "due_date": today + datetime.timedelta(days=15),
        "services": [service_1.id],
        "pdf": pdf1,
    }

    response = client.post(reverse("customers:create-invoice"), data=data)
    assert response.status_code == 302
    assert Invoice.objects.filter(number=1).exists()
    assert response.url == reverse("customers:invoices")


@pytest.mark.django_db
def test_update_invoice_view(client: Client, admin, today, pdf1, invoice_1_with_services, customer_2, service_4):
    """
    Scenario: Update an existing invoice
        Given I am an authenticated administrator
            And I have an existing invoice
        When I submit updated invoice data
            And change the customer and service
        Then the invoice should be updated successfully
            And I should be redirected to the invoice detail page
    """
    client.force_login(admin)
    data = {
        "customer": customer_2.id,
        "number": 1,
        "issue_date": today,
        "delivery_date": today,
        "due_date": today + datetime.timedelta(days=16),
        "services": [service_4.id],
        "pdf": pdf1,
    }

    response = client.post(reverse("customers:update-invoice", kwargs={"pk": invoice_1_with_services.pk}), data=data)
   
    assert response.status_code == 302
    assert Invoice.objects.filter(number=1).exists()
    assert response.url == reverse("customers:invoice", kwargs={"pk": invoice_1_with_services.pk})


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
    response = client.post(reverse("customers:add-service", kwargs={"pk": project_1.pk}), data=data)

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
    response = client.post(reverse("customers:update-service", kwargs={"pk": service_1.pk}), data=data)
    service_1.refresh_from_db()
    assert service_1.time_spent == 0.21
    assert response.status_code == 302
