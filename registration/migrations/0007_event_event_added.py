# Generated by Django 2.1 on 2018-08-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20180808_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_added',
            field=models.BooleanField(default=False),
        ),
    ]