import datetime
from django.urls import reverse
import pytest
from django.test import Client

from customers.models import Invoice


@pytest.mark.django_db
def test_dashboard_url(client: Client, admin):
    client.force_login(admin)
    response = client.get(reverse("customers:dashboard"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_projects_url(client: Client, admin):
    client.force_login(admin)
    response = client.get(reverse("customers:projects"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_invoice_url(client: Client, admin, customer_1, service_1, today, pdf1):
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
