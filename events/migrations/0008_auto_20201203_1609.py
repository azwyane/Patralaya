# Generated by Django 3.1.2 on 2020-12-03 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_bundle_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bundle',
            old_name='likes',
            new_name='claps',
        ),
    ]