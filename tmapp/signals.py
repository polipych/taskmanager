from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from django.core.mail import send_mail
import inspect, os


# @receiver(pre_save, sender=Task)
# def get_user_in_signal(sender, **kwargs):
#     user = None
#     for entry in reversed(inspect.stack()):
#         if os.path.dirname(__file__) + '/admin.py' == entry[1]:
#             try:
#                 user = entry[0].f_locals['request'].user
#             except:
#                 user = None
#             break
#     if user:
#         pass

@receiver(pre_save, sender=Task)
def on_change(sender, instance: Task, **kwargs):
    user = None
    for entry in reversed(inspect.stack()):
        if os.path.dirname(__file__) + '/admin.py' == entry[1]:
            try:
                user = entry[0].f_locals['request'].user
            except:
                user = None
            break
    if user:
        # pass

        if instance.id is None and instance.executor: # new object will be created
            send_mail(f'[TMAPP] Назначение задачи: {instance.subject}',
                    f'{instance.executor.username} Вам назначена задача {instance.keyid}',
                    'tmapp <polipych@yandex.ru>', [instance.executor.email], fail_silently=False)
            # pass # write your code here
        else:
            previous = Task.objects.get(id=instance.id)
            if previous.state != instance.state and previous.executor != instance.executor:
                send_mail(f'[TMAPP] Изменение по задаче: {instance.subject}',
                        f'Пользователь {user.username} внес изменения {instance.task_update.strftime("%d.%m.%Y в %H:%M")}.\nЗадача {instance.keyid} сменила статус: {previous.state} --> {instance.state}.\nНазначен новый исполнитель {instance.executor.username}.',
                        f'{user.username} <polipych@yandex.ru>', [instance.executor.email, previous.executor.email], fail_silently=False)
            elif previous.state != instance.state: # field will be updated
                send_mail(f'[TMAPP] Изменение по задаче: {instance.subject}',
                        f'Пользователь {user.username} внес изменения {instance.task_update.strftime("%d.%m.%Y в %H:%M")}.\nЗадача {instance.keyid} сменила статус: {previous.state} --> {instance.state}.',
                        f'{user.username} <polipych@yandex.ru>', [instance.executor.email], fail_silently=False)
            elif previous.executor != instance.executor:
                send_mail(f'[TMAPP] Изменение по задаче: {instance.subject}',
                        f'Пользователь {user.username} внес изменения {instance.task_update.strftime("%d.%m.%Y в %H:%M")}.\nЗадаче {instance.keyid} назначен новый исполнитель {instance.executor.username}.',
                        f'{user.username} <polipych@yandex.ru>', [instance.executor.email, previous.executor.email], fail_silently=False)