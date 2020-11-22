# Generated by Django 3.1.2 on 2020-11-22 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('profile_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_from', to='profiles.profile')),
                ('profile_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_to', to='profiles.profile')),
            ],
            options={
                'ordering': ('-created_on',),
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='profiles.Follow', to='profiles.Profile'),
        ),
    ]
