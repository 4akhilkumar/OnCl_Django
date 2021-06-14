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

    def __str__(self):
        return self.branch

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.subject_name

GENDER_CHOICES = [
    ("Select Gender", "Select Gender"),
    ("Male", "Male"),
    ("Female", "Female"),
]

BLOOD_GROUP_CHOICES = [
    ("","Blood Group"),
    ("A+","A+"),
    ("A-","A-"),
    ("B+","B+"),
    ("B-","B-"),
    ("O+","O+"),
    ("O-","O-"),
    ("AB+","AB+"),
    ("AB-","AB-"),
]

MOTHER_TOUNGE_CHOICES = [
    ("","Mother Tounge"),
    ("Hindi","Hindi"),
    ("English","English"),
    ("Telugu","Telugu"),
]

BRANCH_CHOICES = [
    ("","Branch Name"),
    ("CSE","Computer Science and Engineering"),
    ("AE","Aerospace/aeronautical Engineering"),
    ("ChE","Chemical Engineering"),
    ("CE","Civil Engineering"),
    ("ECE","Electronics and Communications Engineering"),
]

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
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    father_name = models.CharField(max_length=100, default="")
    father_occ = models.CharField(max_length=100, default="")
    father_phone = models.CharField(max_length=100, default="")
    mother_name = models.CharField(max_length=100, default="")
    mother_tounge = models.CharField(max_length=50, choices = MOTHER_TOUNGE_CHOICES, default=1)
    dob = models.DateField(default='2000-01-01')
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    phone = models.CharField(max_length=100, default="")
    dno_sn = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=100, default="")
    city_name = models.CharField(max_length=50, default="")
    state_name = models.CharField(max_length=50, default="")
    country_name = models.CharField(max_length=50, default="")
    branch = models.CharField(max_length=18, choices = BRANCH_CHOICES, default=1)
    profile_pic = models.ImageField(null=True, blank=True, default="avatar.webp", upload_to='student/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["user__username"]
        
class user_login_details(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - %s' % (self.user.username, self.ip_addr)

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
    sub_an = models.CharField(max_length=100, default="")
    what_an = models.TextField()
    an_image = models.FileField(null=True, blank=True, default='False',upload_to='announcements/')
    an_user = models.CharField(max_length=100, default="")
    an_by = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.sub_an

class E_Books(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.CharField(max_length=100, default="NA")
    book_name = models.CharField(max_length=50, default="NA")
    book_author = models.CharField(max_length=50, default="NA")
    book_author_uid = models.CharField(max_length=50, default="")
    book_pub_date = models.CharField(max_length=20, default="NA")
    book_desc = models.TextField(max_length=255, default="NA")
    book_tag1 = models.CharField(max_length=20, default="NA")
    book_tag2 = models.CharField(max_length=20, default="NA")
    book_tag3 = models.CharField(max_length=20, default="NA")
    book_tag4 = models.CharField(max_length=20, default="NA")
    book_pic = models.ImageField(null=True, blank=True, default='False',upload_to='books/')
    book_file = models.FileField(null=True, blank=True, default='False',upload_to='books/')

    def __str__(self):
        return self.book_name

class PCS_Cloud(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=100, default="NA")
    session_name = models.CharField(max_length=50, default="NA")
    session_author = models.CharField(max_length=50, default="NA")
    session_author_uid = models.CharField(max_length=50, default="")
    session_pub_date = models.CharField(max_length=20, default="NA")
    session_desc = models.TextField(max_length=255, default="NA")
    session_tag1 = models.CharField(max_length=20, default="NA")
    session_tag2 = models.CharField(max_length=20, default="NA")
    session_tag3 = models.CharField(max_length=20, default="NA")
    session_tag4 = models.CharField(max_length=20, default="NA")
    session_pic = models.ImageField(upload_to='sessions/', null=True, blank=True, default="False")
    session_file = models.FileField(upload_to='sessions/', null=True, blank=True, default="False")

    def __str__(self):
        return self.session_name

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

class OnlineClassRoom(models.Model):
    id=models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=255)
    room_pwd=models.CharField(max_length=255)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    started_by=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class AttendanceReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField(default=0)
    branch_id = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    attend_status = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
