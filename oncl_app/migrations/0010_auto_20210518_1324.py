# Generated by Django 3.1.10 on 2021-05-18 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0009_exam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentresult',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='studentresult',
            name='subject_id',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='StudentResult',
        ),
    ]