from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tmapp.models import State, Project, Sprint, Task, User
from simple_history.admin import SimpleHistoryAdmin


class StateAdmin(SimpleHistoryAdmin):
    list_display = ["state_title"]
    history_list_display = ["state_title"]


class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ["title", "key", "author"]
    exclude = ["project_start", "project_end"]
    history_list_display = ["title", "author"]

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.author = request.user
        super(ProjectAdmin, self).save_model(request, obj, form, change)


class SprintAdmin(SimpleHistoryAdmin):
    list_display = ["title", "target", "duration", "sprint_start", "sprint_end"]
    exclude = ["sprint_end"]
    history_list_display = ["title", "target", "duration", "sprint_start", "sprint_end"]


class TaskAdmin(SimpleHistoryAdmin):
    list_display = [
        "keyid",
        "title",
        "body",
        "state",
        "task_start",
        "task_update",
        "executor",
    ]
    exclude = [
        "task_start",
        "task_update",
        "author",
    ]
    history_list_display = ["state", "title", "body", "executor"]

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.author = request.user
        super(TaskAdmin, self).save_model(request, obj, form, change)


admin.site.register(State, StateAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAdmin)
