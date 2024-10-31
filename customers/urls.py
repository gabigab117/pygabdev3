from django.urls import path
from .views import dashboard_view, ProjectList


app_name = "customers"
urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("projects/", ProjectList.as_view(), name="projects")
]
