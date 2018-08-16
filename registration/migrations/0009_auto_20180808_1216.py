# Generated by Django 2.1 on 2018-08-08 12:16

import django.core.files.storage
from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20180808_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='logo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url='/media/logos/', location='/home/allen/Documents/allen/PythonProjects/inter-ed/intered/media/logos/'), upload_to=registration.models.image_directory_path, verbose_name='Logo for the event'),
        ),
    ]