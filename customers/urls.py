from django.urls import path
from .views import dashboard_view, ProjectList, CreateProject, ProjectDetail


app_name = "customers"
urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("projects/", ProjectList.as_view(), name="projects"),
    path("create-project/", CreateProject.as_view(), name="create-project"),
    path("project/<int:pk>/", ProjectDetail.as_view(), name="project")
]