from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Customer, Project


@staff_member_required
def dashboard_view(request):
    customers = Customer.objects.all()
    return render(request, "customers/dashboard.html", context={"customers": customers})


@method_decorator(staff_member_required, name='dispatch')
class ProjectList(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "customers/projects.html"
