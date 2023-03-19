from django.db.models.signals import pre_save
from django.dispatch import receiver
from tmapp.models import Task
from django.core.mail import send_mail
import logging


log = logging.getLogger("emailLogger")


@receiver(pre_save, sender=Task)
def on_change(sender, instance: Task, **kwargs):
    if instance.id is None and instance.executor is None:
        log.info("[SendMail]: Create New Task.")
        send_mail(
            f"[TMAPP] Создана задача: {instance.title}",
            f"Необходимо назначить испольнителя.",
            "tmapp <polipych@yandex.ru>",
            [instance.author.email],
            fail_silently=False,
        )
    elif instance.id is None and instance.executor:
        log.info("[SendMail]: The user is assigned")
        send_mail(
            f"[TMAPP] Назначение задачи: {instance.title}",
            f"{instance.executor.username} Вам назначена задача {instance.title}.",
            "tmapp <polipych@yandex.ru>",
            [instance.executor.email],
            fail_silently=False,
        )
    else:
        previous = Task.objects.get(id=instance.id)
        if previous.state != instance.state and previous.executor != instance.executor:
            log.info("[SendMail]: Сhange of status. The user is assigned.")
            send_mail(
                f"[TMAPP] Изменение по задаче: {instance.title}",
                f'Пользователь {instance.executor} внес изменения {instance.task_update.strftime("%d.%m.%Y в %H:%M")}.\nЗадача {instance.keyid} сменила статус: {previous.state} --> {instance.state}.\nНазначен новый исполнитель {instance.executor.username}.',
                f"{instance.executor} <polipych@yandex.ru>",
                [instance.executor.email, previous.executor.email],
                fail_silently=False,
            )
        elif previous.state != instance.state:
            log.info("[SendMail]: Сhange of status.")
            send_mail(
                f"[TMAPP] Изменение по задаче: {instance.title}",
                f'Пользователь {instance.executor} внес изменения {instance.task_update.strftime("%d.%m.%Y в %H:%M")}.\nЗадача {instance.keyid} сменила статус: {previous.state} --> {instance.state}.',
                f"{instance.executor} <polipych@yandex.ru>",
                [instance.executor.email],
                fail_silently=False,
            )
        elif previous.executor != instance.executor:
            log.info("[SendMail]: The user is assigned.")
            send_mail(
                f"[TMAPP] Изменение по задаче: {instance.title}",
                f'Пользователь {instance.executor} внес изменения {instance.task_update.strftime("%d.%m.%Y в %H:%M")}.\nЗадаче {instance.keyid} назначен новый исполнитель {instance.executor.username}.',
                f"{instance.executor} <polipych@yandex.ru>",
                [instance.executor.email, previous.executor.email],
                fail_silently=False,
            )
