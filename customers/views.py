from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ServiceForm
from .models import Customer, Project, Service


@staff_member_required
def dashboard_view(request):
    customers = Customer.objects.all()
    return render(request, "customers/dashboard.html", context={"customers": customers})


@method_decorator(staff_member_required, name='dispatch')
class ProjectList(ListView):
    model = Project
    template_name = "customers/projects.html"
    paginate_by = 10
    ordering = ["-id"]


@method_decorator(staff_member_required, name='dispatch')
class CreateProject(CreateView):
    model = Project
    template_name = "customers/project_form.html"
    fields = "__all__"
    success_url = reverse_lazy("customers:projects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = "Création d'un projet"
        return context


@method_decorator(staff_member_required, name='dispatch')
class ProjectDetail(DetailView):
    model = Project
    template_name = "customers/project.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(project=self.object)
        return context


@method_decorator(staff_member_required, name='dispatch')
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


@method_decorator(staff_member_required, name='dispatch')
class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy("customers:projects")
    template_name = "customers/project_delete_confirm.html"
    context_object_name = "project"


@method_decorator(staff_member_required, name='dispatch')
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
        context["status"] = f"Mise du service en date du {self.object.date}, projet {self.object.project.name}"
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
        context["projects"] = self.object.projects.all()
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
        context["status"] = f"Création d'un client"
        return context
