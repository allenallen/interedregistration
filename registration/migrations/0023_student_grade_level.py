# Generated by Django 2.1 on 2019-08-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0022_student_registered_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grade_level',
            field=models.IntegerField(blank=True, null=True, verbose_name='Grade Level'),
        ),
    ]