# Generated by Django 3.1.2 on 2020-11-22 08:42

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20201122_1322'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bundle',
            managers=[
                ('objects_publish', django.db.models.manager.Manager()),
            ],
        ),
    ]
