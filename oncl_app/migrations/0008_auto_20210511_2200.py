# Generated by Django 3.1.10 on 2021-05-11 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0007_auto_20210511_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffs',
            old_name='user',
            new_name='admin',
        ),
    ]