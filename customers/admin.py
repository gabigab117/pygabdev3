from django.contrib import admin

from customers.models import Customer, Project, Service, Invoice


class ProjectInline(admin.StackedInline):
    model = Project


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [ProjectInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["project", "date", "time_spent", "billed", "total"]
    list_filter = ["billed", "project"]


class ServiceInline(admin.StackedInline):
    model = Service


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["customer", "name", "hourly_rate"]
    list_filter = ["customer"]
    inlines = [ServiceInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["customer", "number", "issue_date", "total", "paid"]
    list_filter = ["customer", "paid"]
