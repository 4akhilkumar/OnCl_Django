# Generated by Django 3.1.10 on 2021-05-12 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0008_auto_20210511_2200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffs',
            old_name='admin',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='staffs',
            name='address',
            field=models.TextField(),
        ),
    ]
