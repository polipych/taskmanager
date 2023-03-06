from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from simple_history.models import HistoricalRecords
# from django.contrib.auth.models import 
from django.conf import settings


def get_default_task_status():
    """ get a default value for action status; create new status if not available """
    return State.objects.all().first()

class User(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    
    # def get_readonly_fields(self, request, obj=None):
    #     # We make the field uneditable if the user is not a superuser
    #     return super().get_readonly_fields(request) if request.user.is_superuser else ('is_superuser',)
 
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # and also exclude all superusers from queryset if the user is not a superuser
    #     return qs if request.user.is_superuser else qs.exclude(is_superuser=True)

    def __str__(self):
        return self.username

class State(models.Model):

    state_title = models.CharField(max_length=200, null=False, unique=True)
    # weight = models.IntegerField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, default=None)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-parent__id',]

    def __str__(self):
        return self.state_title

# class Status(models.Model):

#     state_title = models.CharField(max_length=200, null=False)
#     # weight = models.IntegerField()
#     parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, default=None)
#     history = HistoricalRecords()

    # class Meta:
    #     ordering = ['-weight',]

    # def __str__(self):
    #     return self.state_title

class Project(models.Model):

    project_title = models.CharField(max_length=80, verbose_name='Проект')
    key = models.CharField(max_length=10, unique=True, verbose_name='Ключ')
    history = HistoricalRecords()

    def __str__(self):
        return self.project_title


class Sprint(models.Model):

    ONEWEEK = '1W'
    TWOWEEK = '2W'
    TREEWEEK = '3W'
    FOURWEEK = '4W'

    DURATION_CHOICES = (
        (ONEWEEK, '1 неделя'),
        (TWOWEEK, '2 недели'),
        (TREEWEEK, '3 недели'),
        (FOURWEEK, '4 недели'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        # related_name='projects',
        verbose_name='Проект',
    )
    sprint_title = models.CharField(max_length=80, verbose_name='Спринт')
    target = models.CharField(max_length=200, verbose_name='Цель спринта')
    duration = models.CharField(
        max_length=8,
        choices=DURATION_CHOICES,
        verbose_name='Длительность',
    )
    sprint_start = models.DateTimeField(
        default=datetime.now(),
        blank=False,
        null=False,
        verbose_name='Дата начала'
    )
    sprint_end = models.DateTimeField(
        default=None,
        blank=False,
        null=False,
        verbose_name='Дата окончания'
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.sprint_title

    def save(self, *args, **kwargs) -> None:
        if self.duration == Sprint.ONEWEEK:
            self.sprint_end = self.sprint_start + timedelta(weeks=1)
        elif self.duration == Sprint.TWOWEEK:
            self.sprint_end = self.sprint_start + timedelta(weeks=2)
        elif self.duration == Sprint.TREEWEEK:
            self.sprint_end = self.sprint_start + timedelta(weeks=3)
        else:
            self.sprint_end = self.sprint_start + timedelta(weeks=4)
        return super().save(*args, **kwargs)

class Task(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        # related_name='projects',
        verbose_name='Проект',
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
        related_name='sprints',
        blank=True,
        null=True,
        verbose_name='Спринт',
    )
    keyid = models.CharField(max_length=20, unique=True, editable=False, verbose_name='ID')
    subject = models.CharField(max_length=160, blank=False, null=False, verbose_name='Задача')
    body = models.TextField(blank=True, null=True, verbose_name='Описание')
    state = models.ForeignKey('State', on_delete=models.PROTECT, default=get_default_task_status, verbose_name='Статус')
    task_start = models.DateTimeField(
        default=datetime.now(),
        verbose_name='Дата создания'
    )
    task_update = models.DateTimeField(
        default=datetime.now(),
        verbose_name='Дата обновления'
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors', editable=False, verbose_name='Автор')
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False}, null=True, blank=True, related_name='executors', verbose_name='Исполнитель')
    history = HistoricalRecords()
    
    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            super().save(*args, **kwargs)
            self.save(*args, **kwargs)
        else:    
            self.keyid = f'{self.project.key}-{self.pk}'
            self.task_update = datetime.now()
            return super().save(*args, **kwargs)
