# Generated by Django 3.1.2 on 2020-12-18 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20201128_1451'),
        ('events', '0014_bundle_co_authors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundle',
            name='co_authors',
            field=models.ManyToManyField(related_name='bundle_co_creators', to='profiles.Profile'),
        ),
    ]
