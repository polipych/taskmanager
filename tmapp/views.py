from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    # DeleteView,
    View,
    TemplateView,
)
from .models import Project, Task, Sprint
from .forms import NewUserForm, AddProjectForm, AddTaskForm, AddSprintForm
from django.contrib.auth import login
from django.contrib.auth import login as authlogin
from django.contrib import messages
from django.db.models import F
from django.db.models import Count
from rest_framework import viewsets
from .serializers import TaskSerializer
from .filters import TaskFilterSet
import logging


log = logging.getLogger("myLogger")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilterSet


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            authlogin(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(
        request=request,
        template_name="registration/register.html",
        context={"register_form": form},
    )


def login(request):
    return redirect("projects")


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_anonymous == True:
            context = super().get_context_data(**kwargs)
            return context
        else:
            context = super().get_context_data(**kwargs)
            context["all_tasks"] = (
                Task.objects.values("project__id")
                .annotate(id=F("project__id"))
                .annotate(all_cnt=Count("id"))
                .order_by("project__id")
                .values("id", "all_cnt")
            )
            context["all_projects"] = Project.objects.all()
            context["all_done_tasks"] = (
                Task.objects.values("project__id")
                .filter(state=3)
                .annotate(id=F("project__id"))
                .annotate(all_cnt_done=Count("id"))
                .order_by("project__id")
                .values("id", "all_cnt_done")
            )
            aggr_projects = []
            for project in context["all_tasks"]:
                for i in list(project):
                    for prjct in context["all_done_tasks"]:
                        if (i in prjct) and (project[i] == prjct[i]):
                            project["all_cnt_done"] = prjct["all_cnt_done"]
                            project["prc"] = round(
                                prjct["all_cnt_done"] * 100 / project["all_cnt"]
                            )
                            context["aggr_projects"] = aggr_projects.append(project)
            log.debug("Open HomeView")
            return context


class ProjectList(ListView):
    model = Project
    context_object_name = "projects_"

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_anonymous == True:
            context = super().get_context_data(**kwargs)
            return context
        else:
            context = super().get_context_data(**kwargs)
            context["all_tasks"] = (
                Task.objects.values("project__id")
                .annotate(id=F("project__id"))
                .annotate(all_cnt=Count("id"))
                .order_by("project__id")
                .values("id", "all_cnt")
            )
            context["executor_projects"] = Project.objects.filter(
                tasksofproject__executor=self.request.user
            ).annotate(n=Count("pk"))
            context["all_done_tasks"] = (
                Task.objects.values("project__id")
                .filter(state=3)
                .annotate(id=F("project__id"))
                .annotate(all_cnt_done=Count("id"))
                .order_by("project__id")
                .values("id", "all_cnt_done")
            )
            aggr_projects = []
            for project in context["all_tasks"]:
                for i in list(project):
                    for prjct in context["all_done_tasks"]:
                        if (i in prjct) and (project[i] == prjct[i]):
                            project["all_cnt_done"] = prjct["all_cnt_done"]
                            project["prc"] = round(
                                prjct["all_cnt_done"] * 100 / project["all_cnt"]
                            )
                            context["aggr_projects"] = aggr_projects.append(project)
            log.debug("Open ProjectListView")
            return context


class ProjectCreate(CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = "project_add.html"
    success_url = "/projects/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        log.debug("Create New Project")
        return redirect("/projects/")


class ProjectEdit(UpdateView):
    model = Project
    fields = ["title", "key"]
    template_name = "project_edit.html"
    success_url = "/projects/"

    def form_valid(self, form):
        messages.success(self.request, "The project was updated successfully.")
        return super(ProjectEdit, self).form_valid(form)


# class ProjectDelete(DeleteView):
#     model = Project
#     template_name = "index.html"
#     success_url = "/projects/"


class ProjectDelete(View):
    success_url = "/projects/"

    def delete(self, request, pk):
        Project.objects.filter(pk=pk).delete()
        return JsonResponse(data={}, status=204)


class TaskList(ListView):
    model = Task
    context_object_name = "tasks_"
    template_name = "tasks.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_anonymous == True:
            context = super().get_context_data(**kwargs)
            return context
        else:
            context = super().get_context_data(**kwargs)
            context["todo"] = Task.objects.all().filter(executor=None)
            context["executor_projects"] = Project.objects.filter(
                tasksofproject__executor=self.request.user
            )
            return context

    def get_queryset(self):
        if self.request.user.is_anonymous == True:
            return Task.objects.all()
        else:
            return Task.objects.filter(executor=self.request.user).order_by("id")


class TaskCreate(CreateView):
    model = Task
    form_class = AddTaskForm
    template_name = "task_add.html"
    success_url = "/tasks/"

    # def sendmail(request):
    #     subject = f"{request.user} send subject"
    #     from_email = my_settings.EMAIL_HOST_USER
    #     to_email = ['admin@gmail.com', 'admin2@gmail.com']
    #     text_content = 'This is an important message.'
    #     # Add your email template here
    #     html_content = '<p>This is an <strong>important</strong> message.</p>'
    #     msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return redirect("/tasks/")


class TaskEdit(UpdateView):
    model = Task
    fields = ["project", "sprint", "title", "body", "state", "executor"]
    template_name = "task_edit.html"
    success_url = "/tasks/"

    def form_valid(self, form):
        messages.success(self.request, "The task was updated successfully.")
        return super(TaskEdit, self).form_valid(form)


class TaskDetails(DetailView):
    model = Task
    template_name = "task_details.html"
    pk_url_kwarg = "pk"
    context_object_name = "task"

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_anonymous == True:
            context = super().get_context_data(**kwargs)
            return context
        else:
            context = super().get_context_data(**kwargs)
            context["detail"] = Task.objects.get(pk=self.kwargs.get("pk"))
        return context


class TaskDelete(View):
    success_url = "/tasks/"

    def delete(self, request, pk):
        Task.objects.filter(pk=pk).delete()
        return JsonResponse(data={}, status=204)


class SprintList(ListView):
    model = Sprint
    context_object_name = "sprints_"
    template_name = "sprints.html"
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_anonymous == True:
            context = super().get_context_data(**kwargs)
            return context
        else:
            context = super().get_context_data(**kwargs)
            context["todo"] = Task.objects.all().filter(executor=None)
            context["executor_sprints"] = Sprint.objects.filter(
                tasksofsprint__executor=self.request.user
            ).annotate(n=Count("pk"))
            for sprint in context["executor_sprints"]:
                context["tasks_sprint"] = Task.objects.filter(sprint_id=sprint.id)
            return context


class SprintCreate(CreateView):
    model = Sprint
    form_class = AddSprintForm
    template_name = "sprint_add.html"
    success_url = "/sprints/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return redirect("/sprints/")


class SprintEdit(UpdateView):
    model = Sprint
    fields = ["project", "title", "target", "duration", "sprint_start"]
    template_name = "sprint_edit.html"
    success_url = "/sprints/"

    def form_valid(self, form):
        messages.success(self.request, "The sprint was updated successfully.")
        return super(SprintEdit, self).form_valid(form)


class SprintDelete(View):
    success_url = "/sprints/"

    def delete(self, request, pk):
        Sprint.objects.filter(pk=pk).delete()
        return JsonResponse(data={}, status=204)
