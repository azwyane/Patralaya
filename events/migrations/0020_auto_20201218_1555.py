# Generated by Django 3.1.2 on 2020-12-18 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_bundle_fork'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundle',
            name='forkable',
            field=models.BooleanField(default=False),
        ),
    ]
