import datetime
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from .factories import CustomerFactory, ProjectFactory, ServiceFactory, InvoiceFactory


User = get_user_model()


@pytest.fixture
def today():
    return datetime.date.today()


@pytest.fixture
def pdf1(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"contenu du PDF")
    return pdf_path


@pytest.fixture
def admin():
    return User.objects.create_superuser(
        username="gabigab", email="g@g.com", password="Test_60000", is_superuser=True
    )


@pytest.fixture
def customer_1():
    return CustomerFactory(name="CustomerTest1")


@pytest.fixture
def customer_2():
    return CustomerFactory(name="CustomerTest2")


@pytest.fixture
def project_1(customer_1):
    return ProjectFactory(customer=customer_1, name="ProjectTest1", hourly_rate=100)


@pytest.fixture
def project_2(customer_1):
    return ProjectFactory(customer=customer_1, name="ProjectTest1", hourly_rate=10)


@pytest.fixture
def project_3(customer_2):
    return ProjectFactory(customer=customer_2, name="ProjectTest1", hourly_rate=10)


@pytest.fixture
def service_1(project_1):
    return ServiceFactory(
        project=project_1,
        date="2024-01-01",
        time_spent=2.0,  # Total sera 200
        description="Service 1 pour Project 1",
    )


@pytest.fixture
def service_2(project_1):
    return ServiceFactory(
        project=project_1,
        date="2024-01-02",
        time_spent=1.5,  # Total sera 150
        description="Service 2 pour Project 1",
    )


@pytest.fixture
def service_3(project_2):
    return ServiceFactory(
        project=project_2,
        date="2024-01-03",
        time_spent=3.0,  # Total sera 30
        description="Service 1 pour Project 2",
    )


@pytest.fixture
def service_4(project_3):
    return ServiceFactory(
        project=project_3,
        date="2024-01-05",
        time_spent=4.0,  # Total sera 40
        description="Service 1 pour Project 3",
    )


@pytest.fixture
def invoice_1(customer_1):
    return InvoiceFactory(
        customer=customer_1,
        number=1,
        issue_date="2024-01-01",
        delivery_date="2024-01-02",
        due_date="2024-02-01",
    )


@pytest.fixture
def invoice_2(customer_1):
    return InvoiceFactory(
        customer=customer_1,
        number=2,
        issue_date="2024-01-15",
        delivery_date="2024-01-16",
        due_date="2024-02-15",
        paid=True,
    )


@pytest.fixture
def invoice_3(customer_2):
    return InvoiceFactory(
        customer=customer_2,
        number=3,
        issue_date="2024-02-01",
        delivery_date="2024-02-02",
        due_date="2024-03-01",
    )


@pytest.fixture
def invoice_1_with_services(invoice_1, service_1, service_2):
    invoice_1.services.add(service_1, service_2)
    invoice_1.update_total()
    return invoice_1


@pytest.fixture
def invoice_2_with_service(invoice_2, service_3):
    invoice_2.services.add(service_3)
    invoice_2.update_total()
    return invoice_2
