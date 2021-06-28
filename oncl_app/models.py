from django.db import models
from django.contrib.auth.models import User

# Note: If migrations didn't detected then use this command -> py manage.py makemigrations app_name

# Create your models here.
BRANCH_CHOICES = [
    ("","Branch Name"),
    ("CSE","Computer Science and Engineering"),
    ("AE","Aerospace/aeronautical Engineering"),
    ("ChE","Chemical Engineering"),
    ("CE","Civil Engineering"),
    ("ECE","Electronics and Communications Engineering"),
]

class Semester(models.Model):
    SEM_MODE = (
        ('EVEN','EVEN'),
        ('ODD','ODD'),
    )
    id = models.AutoField(primary_key=True)
    semester_mode = models.CharField(max_length=4, choices=SEM_MODE)
    branch = models.CharField(max_length=18, choices = BRANCH_CHOICES, default=1)
    semester_start_year = models.DateField()
    semester_end_year = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return '%s %s-%s' % (self.semester_mode, self.semester_start_year.year, self.semester_end_year.year)

class Branches(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    branch = models.CharField(max_length=18, choices = BRANCH_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s' % (self.branch, self.semester)

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=18, choices = BRANCH_CHOICES, default=1)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.subject_name, self.staff_id, self.branch)

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

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    phone = models.CharField(max_length=10, default="9999999999")
    address = models.TextField(default="India")
    qualification = models.CharField(max_length=50, default="M.Tech")
    branch = models.CharField(max_length=18, choices = BRANCH_CHOICES, default=1)
    designation = models.CharField(max_length=50, default="Assistant Professor")
    profile_pic = models.ImageField(null=True, blank=True, default='avatar.webp', upload_to='staffs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name, self.user.last_name)
    
    class Meta:
        ordering = ["user__username"]

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    father_name = models.CharField(max_length=100, default="Not Provided")
    father_occ = models.CharField(max_length=100, default="Not Provided")
    father_phone = models.CharField(max_length=10, default="9999999999")
    mother_name = models.CharField(max_length=100, default="Not Provided")
    mother_tounge = models.CharField(max_length=50, choices = MOTHER_TOUNGE_CHOICES, default=1)
    dob = models.DateField(default='2000-01-01')
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    phone = models.CharField(max_length=10, default="9999999999")
    dno_sn = models.CharField(max_length=100, default="A-BCD, On Earth")
    zip_code = models.CharField(max_length=8, default="123456")
    city_name = models.CharField(max_length=50, default="Vijayawada")
    state_name = models.CharField(max_length=50, default="Andhra Pradesh")
    country_name = models.CharField(max_length=50, default="India")
    branch = models.CharField(max_length=18, choices = BRANCH_CHOICES, default=1)
    profile_pic = models.ImageField(null=True, blank=True, default="avatar.webp", upload_to='student/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ["user__username"]
    
class Student_Social_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=100, default="no_linkedin")
    github = models.CharField(max_length=100, default="no_github")

    def __str__(self):
        return '%s %s %s' % (self.user, self.linkedin, self.github)

class Staff_Social_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=100, default="no_linkedin")
    github = models.CharField(max_length=100, default="no_github")
    orcid = models.CharField(max_length=100, default="no_orcid")
    researcher = models.CharField(max_length=100, default="no_researcher")
    gscholar = models.CharField(max_length=100, default="no_gscholar")
    microsoft_academic = models.CharField(max_length=100, default="no_microsoft_academic")

    def __str__(self):
        return '%s %s %s' % (self.user, self.linkedin, self.gscholar)
    
class user_login_details(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=100)
    os_details = models.CharField(max_length=100)
    browser_details = models.CharField(max_length=100)
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

    def __str__(self):
        return '%s %s' % (self.student_id, self.leave_date)

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=50)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s' % (self.staff_id, self.leave_date)

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
    book_pub_date = models.DateField()
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
    session_pub_date = models.DateField()
    session_desc = models.TextField(max_length=255, default="NA")
    session_tag1 = models.CharField(max_length=20, default="NA")
    session_tag2 = models.CharField(max_length=20, default="NA")
    session_tag3 = models.CharField(max_length=20, default="NA")
    session_tag4 = models.CharField(max_length=20, default="NA")
    session_pic = models.ImageField(upload_to='sessions/', null=True, blank=True, default="False")
    session_file = models.FileField(upload_to='sessions/', null=True, blank=True, default="False")
    created_at = models.DateTimeField(auto_now_add=True)

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
