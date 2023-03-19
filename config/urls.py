"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tmapp.views import (
    ProjectList,
    TaskList,
    register,
    HomeView,
    ProjectCreate,
    ProjectEdit,
    ProjectDelete,
    TaskCreate,
    TaskEdit,
    TaskDetails,
    TaskDelete,
    SprintList,
    SprintCreate,
    SprintEdit,
    SprintDelete,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tmapp.urls")),
    path("", include("django.contrib.auth.urls"), name="login"),
    path("register/", register, name="register"),
    path("", HomeView.as_view(template_name="home.html"), name="home"),
    path(
        "projects/", ProjectList.as_view(template_name="projects.html"), name="projects"
    ),
    path("project/add/", ProjectCreate.as_view(), name="projectcreate"),
    path("project/edit/<int:pk>", ProjectEdit.as_view(), name="projectedit"),
    path("project/delete/<int:pk>", ProjectDelete.as_view(), name="projectdelete"),
    path("tasks/", TaskList.as_view(template_name="tasks.html"), name="tasks"),
    path("task/add/", TaskCreate.as_view(), name="taskcreate"),
    path("task/edit/<int:pk>", TaskEdit.as_view(), name="taskedit"),
    path("task/<int:pk>", TaskDetails.as_view(), name="taskdetails"),
    path("task/delete/<int:pk>", TaskDelete.as_view(), name="taskdelete"),
    path("sprints/", SprintList.as_view(template_name="sprints.html"), name="sprints"),
    path("sprint/add/", SprintCreate.as_view(), name="sprintcreate"),
    path("sprint/edit/<int:pk>", SprintEdit.as_view(), name="sprintedit"),
    path("sprint/delete/<int:pk>", SprintDelete.as_view(), name="sprintdelete"),
]
