# Generated by Django 3.1.10 on 2021-05-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0016_auto_20210519_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancereportstudent',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
