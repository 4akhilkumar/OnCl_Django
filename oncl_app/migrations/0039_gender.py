# Generated by Django 3.1.10 on 2021-05-15 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0038_auto_20210515_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='gender',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('male', models.CharField(default='Male', max_length=4)),
                ('female', models.CharField(default='Female', max_length=6)),
            ],
        ),
    ]
