# Generated by Django 3.1.10 on 2021-05-12 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0019_file_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='profile_image',
            field=models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='users/'),
        ),
    ]