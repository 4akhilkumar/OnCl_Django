# Generated by Django 3.1.10 on 2021-05-11 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0002_sessionyearmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SessionYearModel',
            new_name='Semester',
        ),
        migrations.RenameField(
            model_name='semester',
            old_name='session_end_year',
            new_name='semester_end_year',
        ),
        migrations.RenameField(
            model_name='semester',
            old_name='session_start_year',
            new_name='semester_start_year',
        ),
    ]