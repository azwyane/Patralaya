# Generated by Django 3.1.2 on 2020-11-29 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_bundle_media_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('bundle_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fork_origin', to='events.bundle')),
                ('bundle_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forked_into', to='events.bundle')),
            ],
            options={
                'ordering': ('-created_on',),
            },
        ),
        migrations.AddField(
            model_name='bundle',
            name='fork',
            field=models.ManyToManyField(related_name='forks', through='events.Fork', to='events.Bundle'),
        ),
    ]