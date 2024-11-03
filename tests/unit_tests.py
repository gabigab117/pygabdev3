import pytest

pytestmark = pytest.mark.django_db


def test_total_services(service_1, service_2, service_3, service_4):
    assert service_1.total == 200
    assert service_2.total == 150
    assert service_3.total == 30
    assert service_4.total == 40


def test_total_invoices(invoice_1_with_services, invoice_2_with_service):
    assert invoice_1_with_services.total == 350
    assert invoice_2_with_service.total == 30


def test_if_services_in_invoices_are_billed(invoice_1_with_services, invoice_2_with_service, service_1, service_2):
    service_1.refresh_from_db()
    service_2.refresh_from_db()
    assert service_1.billed
    assert service_2.billed


def test_if_services_are_not_billed(service_1, service_2):
    assert not service_1.billed
    assert not service_2.billed


def test_if_invoice_is_deleted(invoice_1_with_services, service_1, service_2):
    invoice_1_with_services.delete()
    service_1.refresh_from_db()
    service_2.refresh_from_db()
    assert not service_1.billed
    assert not service_2.billed


def test_if_service_1_is_removed(invoice_1_with_services, service_1, service_2):
    invoice_1_with_services.services.remove(service_1)
    service_1.refresh_from_db()
    assert not service_1.billed


def test_if_invoice_is_cleared(invoice_1_with_services, service_1, service_2):
    invoice_1_with_services.services.clear()
    service_1.refresh_from_db()
    service_2.refresh_from_db()
    assert not service_1.billed
    assert not service_2.billed


def test_if_service_is_added(invoice_1, service_1):
    assert not service_1.billed
    invoice_1.services.add(service_1)
    service_1.refresh_from_db()
    assert service_1.billed
