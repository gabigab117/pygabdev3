from django.urls import path
from .views import dashboard_view, ProjectList, CreateProject, ProjectDetail, UpdateProject, DeleteProject, \
    ServiceDetail, CreateService, UpdateService, DeleteService

app_name = "customers"
urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("projects/", ProjectList.as_view(), name="projects"),
    path("create-project/", CreateProject.as_view(), name="create-project"),
    path("project/<int:pk>/", ProjectDetail.as_view(), name="project"),
    path("update-project/<int:pk>/", UpdateProject.as_view(), name="update-project"),
    path("delete-project/<int:pk>/", DeleteProject.as_view(), name="delete-project"),
    path("service/<int:pk>/", ServiceDetail.as_view(), name="service"),
    path("add-service/<int:pk>/", CreateService.as_view(), name="add-service"),
    path("update-service/<int:pk>/", UpdateService.as_view(), name="update-service"),
    path("delete-service/<int:pk>/", DeleteService.as_view(), name="delete-service"),
]
