from django.db import models
from django.contrib.auth.models import User

# Note: If migrations didn't detected then use this command -> py manage.py makemigrations app_name

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    semester_mode = models.CharField(max_length=4, default="")
    semester_start_year = models.DateField()
    semester_end_year = models.DateField()
    objects = models.Manager()

class Branches(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    gender = models.CharField(max_length=6, default="NA")
    phone = models.CharField(max_length=10, default="NA")
    address = models.TextField()
    qualification = models.CharField(max_length=50, default="NA")
    branch = models.CharField(max_length=50, default="NA")
    designation = models.CharField(max_length=50, default="NA")
    git_link = models.CharField(max_length=25, default="NA")
    website_link = models.CharField(max_length=25, default="NA")
    linkedin_link = models.CharField(max_length=50, default="NA")
    orcid_link = models.CharField(max_length=50, default="NA")
    researcher_link = models.CharField(max_length=50, default="NA")
    gscholar_link = models.CharField(max_length=50, default="NA")
    microsoft_academic_link = models.CharField(max_length=50, default="NA")
    bio = models.TextField(default="NA")
    profile_pic = models.ImageField(null=True, blank=True, default='avatar.webp', upload_to='staffs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50, default="NA")
    phone = models.CharField(max_length=50, default="NA")
    address = models.TextField(default="NA")
    branch = models.CharField(max_length=100, default="NA")
    git_link = models.CharField(max_length=50, default="NA")
    website_link = models.CharField(max_length=50, default="NA")
    linkedin_link = models.CharField(max_length=50, default="NA")
    bio = models.TextField(default="NA")
    profile_pic = models.ImageField(null=True, blank=True, default="avatar.webp", upload_to='student/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username

class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=50)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=50)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Announcements_news(models.Model):
    id = models.AutoField(primary_key=True)
    sub_an = models.CharField(max_length=100, default="NA")
    what_an = models.TextField()
    an_by = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class file_upload(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.CharField(max_length=100, default="NA")
    book_name = models.CharField(max_length=50, default="NA")
    book_author = models.CharField(max_length=50, default="NA")
    book_pub_date = models.CharField(max_length=20, default="NA")
    book_desc = models.TextField(max_length=255, default="NA")
    book_tag1 = models.CharField(max_length=20, default="NA")
    book_tag2 = models.CharField(max_length=20, default="NA")
    book_tag3 = models.CharField(max_length=20, default="NA")
    book_tag4 = models.CharField(max_length=20, default="NA")
    book_pic = models.ImageField(null=True, blank=True, default='book.jpg')
    book_file = models.FileField(upload_to='books/')

    def __str__(self):
        return self.book_name

class PCS_Cloud(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=100, default="NA")
    session_name = models.CharField(max_length=50, default="NA")
    session_author = models.CharField(max_length=50, default="NA")
    session_pub_date = models.CharField(max_length=20, default="NA")
    session_desc = models.TextField(max_length=255, default="NA")
    session_tag1 = models.CharField(max_length=20, default="NA")
    session_tag2 = models.CharField(max_length=20, default="NA")
    session_tag3 = models.CharField(max_length=20, default="NA")
    session_tag4 = models.CharField(max_length=20, default="NA")
    session_pic = models.ImageField(null=True, blank=True, default="session.jpg")
    session_file = models.FileField(upload_to='sessions/', default="")

    def __str__(self):
        return self.session_name

class Gender_model(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=11, default="")
    objects = models.Manager()

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    exam_sub = models.CharField(max_length=50)
    ans_file = models.FileField(upload_to='answers/')
    exam_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Exam_ques(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    exam_file = models.FileField(upload_to='question/')
    objects = models.Manager()