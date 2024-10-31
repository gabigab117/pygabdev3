from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

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
