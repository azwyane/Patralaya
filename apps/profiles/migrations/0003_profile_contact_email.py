# Generated by Django 3.1.2 on 2020-12-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20201222_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
