# Generated by Django 3.1.10 on 2021-05-11 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0003_auto_20210511_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branch_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]