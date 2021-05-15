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
    semester_start_year = models.DateField()
    semester_end_year = models.DateField()
    objects = models.Manager()

class Branches(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(default='avatar.webp', upload_to='users/', null=True, blank=True)
    gender = models.CharField(max_length=50, default="Not Updated Yet!")
    phone = models.CharField(max_length=50, default="Not Updated Yet!")
    address = models.TextField()
    qualification = models.CharField(max_length=50, default="Not Updated Yet!")
    branch = models.CharField(max_length=50, default="Not Updated Yet!")
    designation = models.CharField(max_length=50, default="Not Updated Yet!")
    git_link = models.CharField(max_length=50, default="Not Updated Yet!")
    website_link = models.CharField(max_length=50, default="Not Updated Yet!")
    linkedin_link = models.CharField(max_length=50, default="Not Updated Yet!")
    orcid_link = models.CharField(max_length=50, default="Not Updated Yet!")
    researcher_link = models.CharField(max_length=50, default="Not Updated Yet!")
    gscholar_link = models.CharField(max_length=50, default="Not Updated Yet!")
    microsoft_academic_link = models.CharField(max_length=50, default="Not Updated Yet!")
    bio = models.TextField(default="Not Updated Yet!")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    branch = models.CharField(max_length=100, default="Not Updated Yet!")
    gender = models.CharField(max_length=50, default="Not Updated Yet!")
    address = models.TextField(default="Not Updated Yet!")
    phone = models.CharField(max_length=50, default="Not Updated Yet!")
    git_link = models.CharField(max_length=50, default="Not Updated Yet!")
    website_link = models.CharField(max_length=50, default="Not Updated Yet!")
    linkedin_link = models.CharField(max_length=50, default="Not Updated Yet!")
    bio = models.TextField(default="Not Updated Yet!")
    profile_pic = models.ImageField(null=True, blank=True, default="avatar.webp")
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
    sub_an = models.CharField(max_length=100, default="Subject Not Provided!")
    what_an = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class file_upload(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.CharField(max_length=100,default="Not ProvidedYet!")
    book_name = models.CharField(max_length=50,default="Not ProvidedYet!")
    book_author = models.CharField(max_length=50,default="Not ProvidedYet!")
    book_pub_date = models.CharField(max_length=20,default="Not ProvidedYet!")
    book_desc = models.TextField(max_length=255,default="Not ProvidedYet!")
    book_tag1 = models.CharField(max_length=20,default="Not ProvidedYet!")
    book_tag2 = models.CharField(max_length=20,default="Not ProvidedYet!")
    book_tag3 = models.CharField(max_length=20,default="Not ProvidedYet!")
    book_tag4 = models.CharField(max_length=20,default="Not ProvidedYet!")
    book_pic = models.ImageField(null=True, blank=True, default='book.jpeg')
    book_file = models.FileField(upload_to='books/')

    def __str__(self):
        return self.book_name

class PCS_Cloud(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=100,default="Not ProvidedYet!")
    session_name = models.CharField(max_length=50,default="Not ProvidedYet!")
    session_author = models.CharField(max_length=50,default="Not ProvidedYet!")
    session_pub_date = models.CharField(max_length=20,default="Not ProvidedYet!")
    session_desc = models.TextField(max_length=255,default="Not ProvidedYet!")
    session_tag1 = models.CharField(max_length=20,default="Not ProvidedYet!")
    session_tag2 = models.CharField(max_length=20,default="Not ProvidedYet!")
    session_tag3 = models.CharField(max_length=20,default="Not ProvidedYet!")
    session_tag4 = models.CharField(max_length=20,default="Not ProvidedYet!")
    session_pic = models.ImageField(null=True, blank=True, default="session.jpeg")
    session_file = models.FileField(upload_to='sessions/', default="")

    def __str__(self):
        return self.session_name