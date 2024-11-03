from django.urls import path
from .views import dashboard_view, ProjectList, CreateProject, ProjectDetail, UpdateProject, DeleteProject, \
    ServiceDetail, CreateService, UpdateService, DeleteService, CustomerDetail, UpdateCustomer, CreateCustomer, \
    InvoicesList, InvoiceDetail, CreateInvoice, UpdateInvoice, DeleteInvoice

app_name = "customers"
urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("projects/", ProjectList.as_view(), name="projects"),
    path("create-project/", CreateProject.as_view(), name="create-project"),
    path("project/<int:pk>/", ProjectDetail.as_view(), name="project"),
    path("update-project/<int:pk>/", UpdateProject.as_view(), name="update-project"),
    path("delete-project/<int:pk>/", DeleteProject.as_view(), name="delete-project"),
    path("service/<int:pk>/", ServiceDetail.as_view(), name="service"),
    path("add-service/<int:pk>/", CreateService.as_view(), name="add-service"),
    path("update-service/<int:pk>/", UpdateService.as_view(), name="update-service"),
    path("delete-service/<int:pk>/", DeleteService.as_view(), name="delete-service"),
    path("customer/<int:pk>", CustomerDetail.as_view(), name="customer"),
    path("update-customer/<int:pk>", UpdateCustomer.as_view(), name="update-customer"),
    path("create-customer/", CreateCustomer.as_view(), name="create-customer"),
    path("invoices/", InvoicesList.as_view(), name="invoices"),
    path("invoice/<int:pk>/", InvoiceDetail.as_view(), name="invoice"),
    path("create-invoice/", CreateInvoice.as_view(), name="create-invoice"),
    path("update-invoice/<int:pk>/", UpdateInvoice.as_view(), name="update-invoice"),
    path("delete-invoice/<int:pk>/", DeleteInvoice.as_view(), name="delete-invoice"),
]
