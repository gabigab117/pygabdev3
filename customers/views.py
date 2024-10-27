from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import Customer


@staff_member_required
def dashboard_view(request):
    customers = Customer.objects.all()
    return render(request, "customers/dashboard.html", context={"customers": customers})
