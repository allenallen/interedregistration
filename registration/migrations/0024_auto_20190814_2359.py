# Generated by Django 2.1 on 2019-08-14 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0023_student_grade_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='projected_course',
            field=models.CharField(blank=True, help_text='First choice of Course', max_length=200, null=True, verbose_name='Course'),
        ),
    ]
