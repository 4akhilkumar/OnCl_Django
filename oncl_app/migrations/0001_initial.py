# Generated by Django 3.1.10 on 2021-05-16 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements_news',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_an', models.CharField(default='Subject Not Provided!', max_length=100)),
                ('what_an', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branch', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='file_upload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('book_id', models.CharField(default='Not ProvidedYet!', max_length=100)),
                ('book_name', models.CharField(default='Not ProvidedYet!', max_length=50)),
                ('book_author', models.CharField(default='Not ProvidedYet!', max_length=50)),
                ('book_pub_date', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('book_desc', models.TextField(default='Not ProvidedYet!', max_length=255)),
                ('book_tag1', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('book_tag2', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('book_tag3', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('book_tag4', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('book_pic', models.ImageField(blank=True, default='book.jpg', null=True, upload_to='')),
                ('book_file', models.FileField(upload_to='books/')),
            ],
        ),
        migrations.CreateModel(
            name='Gender_model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(default='', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='PCS_Cloud',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.CharField(default='Not ProvidedYet!', max_length=100)),
                ('session_name', models.CharField(default='Not ProvidedYet!', max_length=50)),
                ('session_author', models.CharField(default='Not ProvidedYet!', max_length=50)),
                ('session_pub_date', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('session_desc', models.TextField(default='Not ProvidedYet!', max_length=255)),
                ('session_tag1', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('session_tag2', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('session_tag3', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('session_tag4', models.CharField(default='Not ProvidedYet!', max_length=20)),
                ('session_pic', models.ImageField(blank=True, default='session.jpg', null=True, upload_to='')),
                ('session_file', models.FileField(default='', upload_to='sessions/')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('semester_start_year', models.DateField()),
                ('semester_end_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='oncl_app.branches')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branch', models.CharField(default='Not Updated Yet!', max_length=100)),
                ('gender', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('phone', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('address', models.TextField(default='Not Updated Yet!')),
                ('git_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('website_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('linkedin_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('bio', models.TextField(default='Not Updated Yet!')),
                ('profile_pic', models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_pic', models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='users/')),
                ('gender', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('phone', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('address', models.TextField()),
                ('qualification', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('branch', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('designation', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('git_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('website_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('linkedin_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('orcid_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('researcher_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('gscholar_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('microsoft_academic_link', models.CharField(default='Not Updated Yet!', max_length=50)),
                ('bio', models.TextField(default='Not Updated Yet!')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=50)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncl_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=50)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncl_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'order_with_respect_to': 'user',
            },
        ),
    ]
