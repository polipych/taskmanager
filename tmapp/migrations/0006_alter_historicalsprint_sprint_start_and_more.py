# Generated by Django 4.1.7 on 2023-03-04 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmapp', '0005_alter_historicalsprint_sprint_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsprint',
            name='sprint_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 4, 13, 52, 8, 223820), verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='historicaltask',
            name='task_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 4, 13, 52, 8, 223820), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='historicaltask',
            name='task_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 4, 13, 52, 8, 223820), verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='sprint_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 4, 13, 52, 8, 223820), verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 4, 13, 52, 8, 223820), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 4, 13, 52, 8, 223820), verbose_name='Дата обновления'),
        ),
    ]