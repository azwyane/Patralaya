# Generated by Django 3.1.2 on 2020-11-19 14:46

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('context', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('media_image', models.ImageField(blank=True, null=True, upload_to='bundle_image')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='events.bundle')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
