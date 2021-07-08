# Generated by Django 3.1.12 on 2021-06-30 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oncl_app', '0002_delete_user_login_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_login_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip_addr', models.CharField(max_length=100)),
                ('os_details', models.CharField(max_length=100)),
                ('browser_details', models.CharField(max_length=100)),
                ('device_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]