from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import InvoiceForm, InvoiceUpdateForm, ServiceForm
from .models import Customer, Invoice, Project, Service


@staff_member_required
def dashboard_view(request):
    customers = Customer.objects.all()
    return render(request, "customers/dashboard.html", context={"customers": customers})


@method_decorator(staff_member_required, name="dispatch")
class ProjectList(ListView):
    model = Project
    template_name = "customers/projects.html"
    paginate_by = 10
    ordering = ["-id"]


@method_decorator(staff_member_required, name="dispatch")
class CreateProject(CreateView):
    model = Project
    template_name = "customers/project_form.html"
    fields = "__all__"
    success_url = reverse_lazy("customers:projects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = "Création d'un projet"
        return context


@method_decorator(staff_member_required, name="dispatch")
class ProjectDetail(DetailView):
    model = Project
    template_name = "customers/project.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(project=self.object, billed=False)
        return context


@method_decorator(staff_member_required, name="dispatch")
class UpdateProject(UpdateView):
    model = Project
    template_name = "customers/project_form.html"
    fields = "__all__"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = f"Mise à jour de {self.object.name}"
        return context


@method_decorator(staff_member_required, name="dispatch")
class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy("customers:projects")
    template_name = "customers/project_delete_confirm.html"
    context_object_name = "project"


@method_decorator(staff_member_required, name="dispatch")
class ServiceDetail(DetailView):
    model = Service
    template_name = "customers/service.html"
    context_object_name = "service"


@method_decorator(staff_member_required, name="dispatch")
class CreateService(CreateView):
    model = Service
    template_name = "customers/service_form.html"
    form_class = ServiceForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.project = get_object_or_404(Project, pk=kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = "Création d'un service"
        context["project"] = self.project
        return context

    def get_success_url(self):
        return reverse("customers:project", kwargs={"pk": self.project.pk})


@method_decorator(staff_member_required, name="dispatch")
class UpdateService(UpdateView):
    model = Service
    template_name = "customers/service_form.html"
    form_class = ServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = (
            f"Mise du service en date du {self.object.date}, projet {self.object.project.name}"
        )
        context["project"] = self.object.project
        return context

    def get_success_url(self):
        return reverse("customers:project", kwargs={"pk": self.object.project.pk})


@method_decorator(staff_member_required, name="dispatch")
class DeleteService(DeleteView):
    model = Service
    context_object_name = "service"
    template_name = "customers/service_delete_confirm.html"

    def get_success_url(self):
        return reverse("customers:project", kwargs={"pk": self.object.project.pk})


@method_decorator(staff_member_required, name="dispatch")
class CustomerDetail(DetailView):
    model = Customer
    context_object_name = "customer"
    template_name = "customers/customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = self.object.projects.all()
        context["projects"] = projects
        
        # Services non facturés pour ce client
        unbilled_services = Service.objects.filter(
            project__in=projects, 
            billed=False
        )
        
        # Calcul des totaux
        context["total_unbilled_services"] = unbilled_services.aggregate(
            total_sum=Sum("total")
        )["total_sum"] or 0
        
        context["total_hours_unbilled"] = unbilled_services.aggregate(
            total_hours=Sum("time_spent")
        )["total_hours"] or 0
        
        # Calcul des heures par projet
        projects_hours = []
        for project in projects:
            project_unbilled = unbilled_services.filter(project=project)
            hours = project_unbilled.aggregate(
                total=Sum('time_spent')
            )['total'] or 0
            
            amount = project_unbilled.aggregate(
                total=Sum('total')
            )['total'] or 0
            
            if hours > 0:  # Ajouter seulement si le projet a des heures non facturées
                projects_hours.append({
                    'project': project,
                    'hours': hours,
                    'amount': amount
                })
        
        context["projects_hours"] = projects_hours
        
        return context


@method_decorator(staff_member_required, name="dispatch")
class UpdateCustomer(UpdateView):
    model = Customer
    template_name = "customers/customer_form.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = f"Modifier le client {self.object.name}"
        return context

    def get_success_url(self):
        return reverse("customers:customer", kwargs={"pk": self.object.pk})


@method_decorator(staff_member_required, name="dispatch")
class CreateCustomer(CreateView):
    model = Customer
    template_name = "customers/customer_form.html"
    fields = "__all__"
    success_url = reverse_lazy("customers:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = "Création d'un client"
        return context


@method_decorator(staff_member_required, name="dispatch")
class InvoicesList(ListView):
    model = Invoice
    template_name = "customers/invoices.html"
    paginate_by = 10


@method_decorator(staff_member_required, name="dispatch")
class InvoiceDetail(DetailView):
    model = Invoice
    template_name = "customers/invoice.html"
    context_object_name = "invoice"


@method_decorator(staff_member_required, name="dispatch")
class CreateInvoice(CreateView):
    template_name = "customers/invoice_form.html"
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("customers:invoices")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = "Création d'une facture"
        return context


@method_decorator(staff_member_required, name="dispatch")
class UpdateInvoice(UpdateView):
    model = Invoice
    form_class = InvoiceUpdateForm
    template_name = "customers/invoice_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = (
            f"Mise à jour de la facture {self.object.number}, pour {self.object.customer}"
        )
        return context

    def get_success_url(self):
        return reverse("customers:invoice", kwargs={"pk": self.object.pk})


@method_decorator(staff_member_required, name="dispatch")
class DeleteInvoice(DeleteView):
    model = Invoice
    template_name = "customers/invoice_delete_confirm.html"
    success_url = reverse_lazy("customers:invoices")
    context_object_name = "invoice"


@staff_member_required
def search_view(request):
    customers = Customer.objects.none()
    projects = Project.objects.none()
    services = Service.objects.none()
    invoices = Invoice.objects.none()
    context = {"customers": customers, "projects": projects, "services": services, "invoices": invoices}
    return render(request, "customers/search.html", context=context)


@staff_member_required
def search_results_view(request):
    query = request.GET.get("search", "")

    customers = Customer.objects.none()
    projects = Project.objects.none()
    services = Service.objects.none()
    invoices = Invoice.objects.none()

    if query:
        customers = Customer.objects.filter(name__icontains=query)
        projects = Project.objects.filter(customer__name__icontains=query)
        services = Service.objects.filter(project__customer__name__icontains=query)
        invoices = Invoice.objects.filter(customer__name__icontains=query)
    
    context = {"customers": customers, "projects": projects, "services": services, "invoices": invoices}
    return render(request, "customers/search_results.html", context=context)
