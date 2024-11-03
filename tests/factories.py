from factory.django import DjangoModelFactory
from customers.models import Customer, Project, Service, Invoice


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice
