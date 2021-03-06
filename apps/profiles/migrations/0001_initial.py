# Generated by Django 3.1.2 on 2020-12-22 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ('-created_on',),
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('interest_id', models.PositiveSmallIntegerField(choices=[('science', 'Science'), ('maths', 'Maths'), ('computer', 'Computer'), ('history', 'History'), ('health', 'Health')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='auth.user')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_picture')),
                ('bio', models.TextField(blank=True, null=True)),
                ('current_status', models.CharField(blank=True, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('none', 'Prefer no to say')], max_length=10, null=True)),
                ('following', models.ManyToManyField(related_name='followers', through='profiles.Follow', to='profiles.Profile')),
                ('interest', models.ManyToManyField(to='profiles.Interest')),
            ],
        ),
        migrations.AddField(
            model_name='follow',
            name='profile_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_from', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='profile_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_to', to='profiles.profile'),
        ),
    ]
