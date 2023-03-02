from django.contrib import admin
from tmapp.models import State, Project, Sprint, Task
from simple_history.admin import SimpleHistoryAdmin
from django.core.mail import send_mail


# @admin.register(Project, SimpleHistoryAdmin)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'key']

# @admin.register(Sprint, SimpleHistoryAdmin)
# class SprintAdmin(admin.ModelAdmin):
#     list_display = ['title', 'target', 'duration', 'sprint_start', 'sprint_end']
#     exclude = ['sprint_end']

# @admin.register(Task, SimpleHistoryAdmin)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['id', 'keyid', 'subject', 'body' , 'status', 'task_start', 'task_update']
#     history_list_display = ['status']


class StateAdmin(SimpleHistoryAdmin):
    list_display = ['state_title']
    history_list_display = ['state_title']
    # state = State.objects.create(state_title="Тестирование")

# class StatusAdmin(Status):
#     list_display = ['state_title']
#     history_list_display = ['state_title']
    # state = State.objects.create(name="Тестирование")

class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ['project_title', 'key']


class SprintAdmin(SimpleHistoryAdmin):
    list_display = ['sprint_title', 'target', 'duration', 'sprint_start', 'sprint_end']
    exclude = ['sprint_end']
    history_list_display = ['title', 'target', 'duration', 'sprint_start', 'sprint_end']


class TaskAdmin(SimpleHistoryAdmin):
    list_display = ['keyid', 'subject', 'body' , 'state', 'task_start', 'task_update', 'author', 'executor']
    exclude = ['task_start', 'task_update']
    history_list_display = ['state', 'subject', 'body', 'executor']

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.author = request.user
            # send_mail('Django mail', 'This e-mail was sent with Django.', 'tmapp <polipych@yandex.ru>', [obj.author.email], fail_silently=False)
        super(TaskAdmin, self).save_model(request, obj, form, change)

admin.site.register(State, StateAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Task, TaskAdmin)
# admin.site.register(Status)
