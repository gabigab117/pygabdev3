from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.db.models import Count, Sum
from django.template.response import TemplateResponse
from django.utils.formats import number_format

from customers.models import Customer, Invoice, Project, Service


class ProjectInline(admin.StackedInline):
    model = Project


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [ProjectInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["project", "date", "time_spent", "billed", "total"]
    list_filter = ["billed", "project__customer", "project"]
    actions = ["mark_as_billed"]

    @admin.action(description="Marquer comme facturés", permissions=["change"])
    def mark_as_billed(self, request, queryset):
        # Two steps, like Django's delete_selected: a confirmation page with the
        # amount, then the change once it is posted back with "post".
        to_bill = queryset.filter(billed=False)
        totals = to_bill.aggregate(
            count=Count("pk"), total=Sum("total"), hours=Sum("time_spent")
        )
        if not totals["count"]:
            self.message_user(
                request, "Aucun service à facturer dans la sélection.", messages.WARNING
            )
            return None

        if request.POST.get("post"):
            # update() skips save() and the signals: harmless here, an unbilled
            # service is on no invoice.
            to_bill.update(billed=True)
            self.message_user(
                request,
                f"Services marqués facturés : {totals['count']}, "
                f"pour {number_format(totals['total'], 2)} €.",
                messages.SUCCESS,
            )
            return None

        return TemplateResponse(
            request,
            "admin/customers/service/mark_as_billed_confirmation.html",
            {
                **self.admin_site.each_context(request),
                "title": "Marquer des services comme facturés",
                "opts": self.opts,
                "services": to_bill.select_related("project__customer"),
                "ignored": queryset.count() - totals["count"],
                "total": totals["total"],
                "hours": totals["hours"],
                "action_checkbox_name": ACTION_CHECKBOX_NAME,
            },
        )


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

    # Invoices are now made on facture.net: the old ones stay as a read-only archive.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
