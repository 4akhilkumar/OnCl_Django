# Generated by Django 3.1.12 on 2021-07-07 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceReportStudent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('student_id', models.IntegerField(default=0)),
                ('branch_id', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('attend_status', models.IntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('branch', models.CharField(choices=[('', 'Branch Name'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Aerospace/aeronautical Engineering', 'Aerospace/aeronautical Engineering'), ('Chemical Engineering', 'Chemical Engineering'), ('Civil Engineering', 'Civil Engineering'), ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Petroleum Engineering', 'Petroleum Engineering'), ('Bio Technology', 'Bio Technology'), ('Mechanical Engineering', 'Mechanical Engineering')], default=1, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('section_name', models.CharField(max_length=100)),
                ('room_no', models.CharField(max_length=100)),
                ('floor_no', models.CharField(choices=[('', 'Select Floor'), ('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th')], max_length=4)),
                ('block_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('semester_mode', models.CharField(choices=[('EVEN', 'EVEN'), ('ODD', 'ODD')], max_length=4)),
                ('branch', models.CharField(choices=[('', 'Branch Name'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Aerospace/aeronautical Engineering', 'Aerospace/aeronautical Engineering'), ('Chemical Engineering', 'Chemical Engineering'), ('Civil Engineering', 'Civil Engineering'), ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Petroleum Engineering', 'Petroleum Engineering'), ('Bio Technology', 'Bio Technology'), ('Mechanical Engineering', 'Mechanical Engineering')], default=1, max_length=50)),
                ('semester_start_year', models.DateField()),
                ('semester_end_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='user_login_details',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_ip_address', models.CharField(max_length=100)),
                ('os_details', models.CharField(max_length=100)),
                ('browser_details', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=50, unique=True)),
                ('branch', models.CharField(choices=[('', 'Branch Name'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Aerospace/aeronautical Engineering', 'Aerospace/aeronautical Engineering'), ('Chemical Engineering', 'Chemical Engineering'), ('Civil Engineering', 'Civil Engineering'), ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Petroleum Engineering', 'Petroleum Engineering'), ('Bio Technology', 'Bio Technology'), ('Mechanical Engineering', 'Mechanical Engineering')], default=1, max_length=50)),
                ('desc', models.TextField(blank=True, null=True)),
                ('semester', models.ManyToManyField(to='oncl_app.Semester')),
                ('staff_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')], default=1, max_length=14)),
                ('father_name', models.CharField(default='Not Provided', max_length=100)),
                ('father_occ', models.CharField(default='Not Provided', max_length=100)),
                ('father_phone', models.CharField(default='9999999999', max_length=10)),
                ('mother_name', models.CharField(default='Not Provided', max_length=100)),
                ('mother_tounge', models.CharField(choices=[('', 'Mother Tounge'), ('Hindi', 'Hindi'), ('English', 'English'), ('Telugu', 'Telugu')], default=1, max_length=50)),
                ('dob', models.DateField(default='1998-01-01')),
                ('blood_group', models.CharField(choices=[('', 'Blood Group'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], default=1, max_length=18)),
                ('phone', models.CharField(default='9999999999', max_length=10)),
                ('dno_sn', models.CharField(default='A-BCD, On Earth', max_length=100)),
                ('zip_code', models.CharField(default='123456', max_length=8)),
                ('city_name', models.CharField(default='Vijayawada', max_length=50)),
                ('state_name', models.CharField(default='Andhra Pradesh', max_length=50)),
                ('country_name', models.CharField(default='India', max_length=50)),
                ('branch', models.CharField(choices=[('', 'Branch Name'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Aerospace/aeronautical Engineering', 'Aerospace/aeronautical Engineering'), ('Chemical Engineering', 'Chemical Engineering'), ('Civil Engineering', 'Civil Engineering'), ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Petroleum Engineering', 'Petroleum Engineering'), ('Bio Technology', 'Bio Technology'), ('Mechanical Engineering', 'Mechanical Engineering')], default=1, max_length=50)),
                ('profile_pic', models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='student/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
        migrations.CreateModel(
            name='Student_Social_Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('linkedin', models.CharField(default='no_linkedin', max_length=100)),
                ('github', models.CharField(default='no_github', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Sem_Reg',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.semester')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Course_Reg',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.sections')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.subjects')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')], default=1, max_length=14)),
                ('father_name', models.CharField(default='Not Provided', max_length=100)),
                ('father_occ', models.CharField(default='Not Provided', max_length=100)),
                ('father_phone', models.CharField(default='9999999999', max_length=10)),
                ('mother_name', models.CharField(default='Not Provided', max_length=100)),
                ('mother_tounge', models.CharField(choices=[('', 'Mother Tounge'), ('Hindi', 'Hindi'), ('English', 'English'), ('Telugu', 'Telugu')], default=1, max_length=50)),
                ('dob', models.DateField(default='1975-01-01')),
                ('blood_group', models.CharField(choices=[('', 'Blood Group'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], default=1, max_length=18)),
                ('phone', models.CharField(default='9999999999', max_length=10)),
                ('dno_sn', models.CharField(default='A-BCD, On Earth', max_length=100)),
                ('zip_code', models.CharField(default='123456', max_length=8)),
                ('city_name', models.CharField(default='Vijayawada', max_length=50)),
                ('state_name', models.CharField(default='Andhra Pradesh', max_length=50)),
                ('country_name', models.CharField(default='India', max_length=50)),
                ('qualification', models.CharField(default='M.Tech', max_length=50)),
                ('branch', models.CharField(choices=[('', 'Branch Name'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Aerospace/aeronautical Engineering', 'Aerospace/aeronautical Engineering'), ('Chemical Engineering', 'Chemical Engineering'), ('Civil Engineering', 'Civil Engineering'), ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Petroleum Engineering', 'Petroleum Engineering'), ('Bio Technology', 'Bio Technology'), ('Mechanical Engineering', 'Mechanical Engineering')], default=1, max_length=50)),
                ('designation', models.CharField(default='Assistant Professor', max_length=50)),
                ('profile_pic', models.ImageField(blank=True, default='avatar.webp', null=True, upload_to='staffs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
        migrations.CreateModel(
            name='Staff_Social_Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('linkedin', models.CharField(default='no_linkedin', max_length=100)),
                ('github', models.CharField(default='no_github', max_length=100)),
                ('orcid', models.CharField(default='no_orcid', max_length=100)),
                ('researcher', models.CharField(default='no_researcher', max_length=100)),
                ('gscholar', models.CharField(default='no_gscholar', max_length=100)),
                ('microsoft_academic', models.CharField(default='no_microsoft_academic', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PCS_Cloud',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_ref_no', models.CharField(default='4488', max_length=13)),
                ('session_name', models.CharField(default='Enterprise Programming', max_length=50)),
                ('session_desc', models.TextField(default='Java Enterprise edition has changed and evolved a lot over the years. This course is about teaching you what JEE is, and how to use it and become a productive JEE developer. The course focuses on JEE 8 (also known as Jakarta EE).', max_length=255)),
                ('session_pub_date', models.DateField(default='2021-04-04')),
                ('session_tag1', models.CharField(default='Java', max_length=25)),
                ('session_tag2', models.CharField(default='Enterprise Programming', max_length=25)),
                ('session_tag3', models.CharField(default='Web Services', max_length=25)),
                ('session_tag4', models.CharField(default='Testing - Java', max_length=25)),
                ('session_pic', models.ImageField(blank=True, default='False', null=True, upload_to='sessions/')),
                ('session_file', models.FileField(blank=True, default='False', null=True, upload_to='sessions/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='OnlineClassRoom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=255)),
                ('room_pwd', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('started_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.staffs')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=50)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStaff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=50)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='Exam_ques',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('exam_file', models.FileField(upload_to='question/')),
                ('subject_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('exam_sub', models.CharField(max_length=50)),
                ('ans_file', models.FileField(upload_to='answers/')),
                ('exam_marks', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oncl_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='E_Books',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('book_id', models.CharField(default='B079ZZLRRL', max_length=13)),
                ('book_name', models.CharField(default='Django for Beginners: Build websites with Python and Django', max_length=100)),
                ('book_author', models.CharField(default='William S. Vincent', max_length=100)),
                ('book_pub_date', models.DateField(default='2018-03-07')),
                ('book_desc', models.TextField(default='Django for Beginners is a project-based introduction to Django, the popular Python-based web framework. Suitable for total beginners who have never built a website before as well as professional programmers looking for a fast-paced guide to modern web development and Django fundamentals.', max_length=255)),
                ('book_tag1', models.CharField(default='William S. Vincent', max_length=20)),
                ('book_tag2', models.CharField(default='Django', max_length=20)),
                ('book_tag3', models.CharField(default='Python', max_length=20)),
                ('book_tag4', models.CharField(default='Web Application', max_length=20)),
                ('book_pic', models.ImageField(blank=True, default='False', null=True, upload_to='books/')),
                ('book_file', models.FileField(default='False', upload_to='books/')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcements_news',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_an', models.CharField(default='', max_length=100)),
                ('what_an', models.TextField()),
                ('an_image', models.FileField(blank=True, default='False', null=True, upload_to='announcements/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
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
