# Generated by Django 3.1.10 on 2021-05-16 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncl_app', '0006_auto_20210516_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcements_news',
            name='an_by',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='semester',
            name='semester_mode',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='announcements_news',
            name='sub_an',
            field=models.CharField(default='NA', max_length=100),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_author',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_desc',
            field=models.TextField(default='NA', max_length=255),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_id',
            field=models.CharField(default='NA', max_length=100),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_name',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_pub_date',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_tag1',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_tag2',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_tag3',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='file_upload',
            name='book_tag4',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_author',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_desc',
            field=models.TextField(default='NA', max_length=255),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_id',
            field=models.CharField(default='NA', max_length=100),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_name',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_pub_date',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_tag1',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_tag2',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_tag3',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='pcs_cloud',
            name='session_tag4',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='bio',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='branch',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='designation',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='gender',
            field=models.CharField(default='NA', max_length=6),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='git_link',
            field=models.CharField(default='NA', max_length=25),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='gscholar_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='linkedin_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='microsoft_academic_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='orcid_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='phone',
            field=models.CharField(default='NA', max_length=10),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='profile_pic',
            field=models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='staffs/'),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='qualification',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='researcher_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='website_link',
            field=models.CharField(default='NA', max_length=25),
        ),
        migrations.AlterField(
            model_name='students',
            name='address',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='students',
            name='bio',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='students',
            name='branch',
            field=models.CharField(default='NA', max_length=100),
        ),
        migrations.AlterField(
            model_name='students',
            name='gender',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='students',
            name='git_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='students',
            name='linkedin_link',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='students',
            name='phone',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='student/'),
        ),
        migrations.AlterField(
            model_name='students',
            name='website_link',
            field=models.CharField(default='NA', max_length=50),
        ),
    ]