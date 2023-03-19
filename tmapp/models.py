from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta, timezone
from simple_history.models import HistoricalRecords

# from django.contrib.auth.models import
from django.conf import settings


def get_default_task_status():
    """get a default value for action status; create new status if not available"""
    return State.objects.all().first()


class User(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.username


class State(models.Model):
    state_title = models.CharField(max_length=200, null=False, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, default=None
    )
    history = HistoricalRecords()

    class Meta:
        ordering = [
            "-parent__id",
        ]

    def __str__(self):
        return self.state_title


class Project(models.Model):
    title = models.CharField(max_length=80, verbose_name="Проект")
    key = models.CharField(max_length=10, unique=True, verbose_name="Ключ")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        blank=True,
        null=True,
        verbose_name="Автор",
    )
    project_start = models.DateTimeField(
        default=datetime.now, blank=False, null=False, verbose_name="Дата начала"
    )
    project_end = models.DateTimeField(
        default=None, blank=True, null=True, verbose_name="Дата окончания"
    )
    history = HistoricalRecords()

    @property
    def duration(self):
        return (datetime.now() - self.project_start).days

    def __str__(self):
        return self.title


class Sprint(models.Model):
    ONEWEEK = "1W"
    TWOWEEK = "2W"
    TREEWEEK = "3W"
    FOURWEEK = "4W"

    DURATION_CHOICES = (
        (ONEWEEK, "1 неделя"),
        (TWOWEEK, "2 недели"),
        (TREEWEEK, "3 недели"),
        (FOURWEEK, "4 недели"),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sprintsofproject",
        verbose_name="Проект",
    )
    title = models.CharField(max_length=80, verbose_name="Спринт")
    target = models.CharField(max_length=200, verbose_name="Цель спринта")
    duration = models.CharField(
        max_length=8,
        choices=DURATION_CHOICES,
        verbose_name="Длительность",
    )
    sprint_start = models.DateTimeField(
        default=datetime.now, blank=False, null=False, verbose_name="Дата начала"
    )
    sprint_end = models.DateTimeField(
        default=None, blank=False, null=False, verbose_name="Дата окончания"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.title

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
        related_name="tasksofproject",
        verbose_name="Проект",
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
        related_name="tasksofsprint",
        blank=True,
        null=True,
        verbose_name="Спринт",
    )
    keyid = models.CharField(
        max_length=20, unique=True, editable=False, verbose_name="ID"
    )
    title = models.CharField(
        max_length=160, blank=False, null=False, verbose_name="Задача"
    )
    body = models.TextField(blank=True, null=True, verbose_name="Описание")
    state = models.ForeignKey(
        "State",
        on_delete=models.PROTECT,
        default=get_default_task_status,
        verbose_name="Статус",
    )
    task_start = models.DateTimeField(
        default=datetime.now, verbose_name="Дата создания"
    )
    task_update = models.DateTimeField(
        default=datetime.now, verbose_name="Дата обновления"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_superuser": False},
        null=True,
        blank=True,
        related_name="executors",
        verbose_name="Исполнитель",
    )
    history = HistoricalRecords()

    class Meta:
        ordering = [
            "task_start",
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.task_update = datetime.now()
        super().save(*args, **kwargs)
        self.set_key()

    def set_key(self, *args, **kwargs):
        self.keyid = f"{self.project.key}-{self.pk}"
        return super().save(*args, **kwargs)
