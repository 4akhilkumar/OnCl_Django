# Generated by Django 3.1.10 on 2021-05-15 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0036_auto_20210515_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='branch',
            field=models.CharField(default='Not Updated Yet!', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='designation',
            field=models.CharField(default='Not Updated Yet!', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='gender',
            field=models.CharField(default='Not Updated Yet!', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='phone',
            field=models.CharField(default='Not Updated Yet!', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='qualification',
            field=models.CharField(default='Not Updated Yet!', max_length=50),
        ),
    ]