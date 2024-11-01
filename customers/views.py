from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
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


@staff_member_required
def add_service_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    status = "Création d'un service"
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.project = project
            service.save()
            return redirect(project)
    else:
        form = ServiceForm()
    return render(request, "customers/service_form.html", context={"form": form, "status": status})
