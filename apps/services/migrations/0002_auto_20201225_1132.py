# Generated by Django 3.1.2 on 2020-12-25 05:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinglist',
            name='uuid',
            field=models.SlugField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
