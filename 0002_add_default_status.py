# Generated by Django 4.1.6 on 2023-02-21 06:51

from django.db import migrations, models
from django.db import IntegrityError, transaction


def set_default_status(apps, schema_editor):
    # Статусы - перечень, который будет вставлен в БД
    statuses = {None: "ToDo", 1: "In Work", 2: "Done"}
    # statuses = ['К выполнению', 'В работе', 'Готово']
    # Запрашиваем модель - класс State из аппликейшена tmapp
    State = apps.get_model("tmapp", "State")

    # В цикле создаём экземпляры класса с указанными параметрами и сохраняем их
    for key, value in statuses.items():
        try:
            with transaction.atomic():
                State.objects.create(state_title=value, parent_id=key)
        except IntegrityError:
            pass
    # for element in statuses:
    #     try:
    #         with transaction.atomic():
    #             State.objects.create(state_title=element)
    #     except IntegrityError:
    #         pass


def delete_default_status(apps, schema_editor):
    # Запрашиваем модель - класс State из аппликейшена tmapp
    State = apps.get_model("tmapp", "State")

    # Удаляем ранее созданные экземпляры класса
    State.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tmapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_default_status, reverse_code=delete_default_status),
    ]
