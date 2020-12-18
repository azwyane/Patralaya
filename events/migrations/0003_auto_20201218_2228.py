# Generated by Django 3.1.2 on 2020-12-18 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20201128_1451'),
        ('events', '0002_auto_20201218_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundle',
            name='co_authors',
            field=models.ManyToManyField(related_name='bundle_co_creators', through='events.AcceptedAuthorshipRequest', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='co_authors_request',
            field=models.ManyToManyField(related_name='bundle_co_creators_requests', through='events.ReceivedAuthorshipRequest', to='profiles.Profile'),
        ),
    ]
