from django.db import models
from django.contrib.auth.models import User
import uuid

# Note: If migrations didn't detected then use this command -> py manage.py makemigrations app_name

# Create your models here.
BRANCH_CHOICES = [
    ("","Branch Name"),
    ("Computer Science and Engineering","Computer Science and Engineering"),
    ("Aerospace/aeronautical Engineering","Aerospace/aeronautical Engineering"),
    ("Chemical Engineering","Chemical Engineering"),
    ("Civil Engineering","Civil Engineering"),
    ("Electronics and Communications Engineering","Electronics and Communications Engineering"),
    ("Electrical and Electronics Engineering","Electrical and Electronics Engineering"),
    ("Petroleum Engineering","Petroleum Engineering"),
    ("Bio Technology","Bio Technology"),
    ("Mechanical Engineering","Mechanical Engineering"),
]

class Branches(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.CharField(max_length=50, unique=True, choices = BRANCH_CHOICES, default=1)
    objects = models.Manager()

    def __str__(self):
        return '%s' % (self.branch)

class Semester(models.Model):
    SEM_MODE = (
        ('EVEN','EVEN'),
        ('ODD','ODD'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester_mode = models.CharField(max_length=4, choices=SEM_MODE)
    branch = models.CharField(max_length=50, choices = BRANCH_CHOICES, default=1)
    semester_start_year = models.DateField()
    semester_end_year = models.DateField()
    objects = models.Manager()

    def __str__(self):
        branch_split = self.branch.split(" ")
        branch_split.remove('and')
        str_branch_split = ""
        for i in branch_split:
            str_branch_split += i[0]
        return '%s %s %s-%s' % (str_branch_split, self.semester_mode, self.semester_start_year.year, self.semester_end_year.year)

GENDER_CHOICES = [
    ("", "Select Gender"),
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    father_name = models.CharField(max_length=100, default="Not Provided")
    father_occ = models.CharField(max_length=100, default="Not Provided")
    father_phone = models.CharField(max_length=10, default="9999999999")
    mother_name = models.CharField(max_length=100, default="Not Provided")
    mother_tounge = models.CharField(max_length=50, choices = MOTHER_TOUNGE_CHOICES, default=1)
    dob = models.DateField(default='1975-01-01')
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    phone = models.CharField(max_length=10, default="9999999999")
    dno_sn = models.CharField(max_length=100, default="A-BCD, On Earth")
    zip_code = models.CharField(max_length=8, default="123456")
    city_name = models.CharField(max_length=50, default="Vijayawada")
    state_name = models.CharField(max_length=50, default="Andhra Pradesh")
    country_name = models.CharField(max_length=50, default="India")
    qualification = models.CharField(max_length=50, default="M.Tech")
    branch = models.CharField(max_length=50, choices = BRANCH_CHOICES, default=1)
    designation = models.CharField(max_length=50, default="Assistant Professor")
    profile_pic = models.ImageField(null=True, blank=True, default='avatar.webp', upload_to='staffs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["user__username"]

class Subjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=50, choices = BRANCH_CHOICES, default=1)
    semester = models.ManyToManyField(Semester)
    staff_id = models.ManyToManyField(Staffs)
    desc = models.TextField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % (self.subject_name)

class Students(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    father_name = models.CharField(max_length=100, default="Not Provided")
    father_occ = models.CharField(max_length=100, default="Not Provided")
    father_phone = models.CharField(max_length=10, default="9999999999")
    mother_name = models.CharField(max_length=100, default="Not Provided")
    mother_tounge = models.CharField(max_length=50, choices = MOTHER_TOUNGE_CHOICES, default=1)
    dob = models.DateField(default='1998-01-01')
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    phone = models.CharField(max_length=10, default="9999999999")
    dno_sn = models.CharField(max_length=100, default="A-BCD, On Earth")
    zip_code = models.CharField(max_length=8, default="123456")
    city_name = models.CharField(max_length=50, default="Vijayawada")
    state_name = models.CharField(max_length=50, default="Andhra Pradesh")
    country_name = models.CharField(max_length=50, default="India")
    branch = models.CharField(max_length=50, choices = BRANCH_CHOICES, default=1)
    profile_pic = models.ImageField(null=True, blank=True, default="avatar.webp", upload_to='student/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())

    class Meta:
        ordering = ["user__username"]
    
class Student_Social_Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Students, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=100, default="no_linkedin")
    github = models.CharField(max_length=100, default="no_github")

    def __str__(self):
        return '%s %s %s' % (self.user.user.username, self.linkedin, self.github)

class Staff_Social_Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=100, default="no_linkedin")
    github = models.CharField(max_length=100, default="no_github")
    orcid = models.CharField(max_length=100, default="no_orcid")
    researcher = models.CharField(max_length=100, default="no_researcher")
    gscholar = models.CharField(max_length=100, default="no_gscholar")
    microsoft_academic = models.CharField(max_length=100, default="no_microsoft_academic")

    def __str__(self):
        return '%s %s %s' % (self.user.user.username, self.linkedin, self.gscholar)

FLOORS = [
    ("","Select Floor"),
    ("1st","1st"),
    ("2nd","2nd"),
    ("3rd","3rd"),
    ("4th","4th"),
    ("5th","5th"),
    ("6th","6th"),
]

class Sections(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section_name = models.CharField(max_length=100)
    room_no = models.CharField(max_length=100)
    floor_no = models.CharField(max_length=4, choices = FLOORS)
    block_name = models.CharField(max_length=100)

    def __str__(self):
        return 'Section %s, %s %s' % (self.section_name, self.room_no, self.block_name)

class Student_Sem_Reg(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.user, self.semester.all().count())

class Student_Course_Reg(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Staffs, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Sections, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.user.user, self.subject)

class user_login_details(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    user_ip_address = models.CharField(max_length=100)
    os_details = models.CharField(max_length=100)
    browser_details = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - %s' % (self.user, self.user_ip_address)

class LeaveReportStudent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey(Students, on_delete=models.SET_NULL, blank=True, null=True)
    leave_date = models.CharField(max_length=50)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s' % (self.student_id, self.leave_date)

class LeaveReportStaff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_id = models.ForeignKey(Staffs, on_delete=models.SET_NULL, blank=True, null=True)
    leave_date = models.CharField(max_length=50)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s' % (self.staff_id, self.leave_date)

class Announcements_news(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_an = models.CharField(max_length=100, default="")
    what_an = models.TextField()
    an_image = models.FileField(null=True, blank=True, default='False',upload_to='announcements/')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.sub_an

class E_Books(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_id = models.CharField(max_length=13, default="B079ZZLRRL")
    book_name = models.CharField(max_length=100, default="Django for Beginners: Build websites with Python and Django")
    book_author = models.CharField(max_length=100, default="William S. Vincent")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    book_pub_date = models.DateField(default="2018-03-07")
    book_desc = models.TextField(max_length=500, default="Django for Beginners is a project-based introduction to Django, the popular Python-based web framework. Suitable for total beginners who have never built a website before as well as professional programmers looking for a fast-paced guide to modern web development and Django fundamentals.")
    book_tag1 = models.CharField(max_length=20, default="William S. Vincent")
    book_tag2 = models.CharField(max_length=20, default="Django")
    book_tag3 = models.CharField(max_length=20, default="Python")
    book_tag4 = models.CharField(max_length=20, default="Web Application")
    book_pic = models.ImageField(null=True, blank=True, default='False',upload_to='books/')
    book_file = models.FileField(default='False',upload_to='books/')

    def __str__(self):
        return self.book_name

class PCS_Cloud(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_ref_no = models.CharField(max_length=13, default="4488")
    session_name = models.CharField(max_length=50, default="Enterprise Programming")
    session_desc = models.TextField(max_length=500, default="Java Enterprise edition has changed and evolved a lot over the years. This course is about teaching you what JEE is, and how to use it and become a productive JEE developer. The course focuses on JEE 8 (also known as Jakarta EE).")
    session_pub_date = models.DateField(default="2021-04-04")
    user = models.ForeignKey(Staffs, on_delete=models.SET_NULL, blank=True, null=True)
    session_tag1 = models.CharField(max_length=25, default="Java")
    session_tag2 = models.CharField(max_length=25, default="Enterprise Programming")
    session_tag3 = models.CharField(max_length=25, default="Web Services")
    session_tag4 = models.CharField(max_length=25, default="Testing - Java")
    session_pic = models.ImageField(upload_to='sessions/', null=True, blank=True, default="False")
    session_file = models.FileField(upload_to='sessions/', null=True, blank=True, default="False")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.session_name, self.user.user.first_name)

class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey(Students, on_delete=models.SET_NULL, blank=True, null=True)
    exam_sub = models.CharField(max_length=50)
    ans_file = models.FileField(upload_to='answers/')
    exam_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Exam_ques(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_id = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True)
    exam_file = models.FileField(upload_to='question/')
    objects = models.Manager()

class OnlineClassRoom(models.Model):
    id=models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=255)
    room_pwd=models.CharField(max_length=255)
    subject=models.ForeignKey(Subjects,on_delete=models.SET_NULL, blank=True, null=True)
    started_by=models.ForeignKey(Staffs,on_delete=models.SET_NULL, blank=True, null=True)
    is_active=models.BooleanField(default=True)
    created_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class AttendanceReportStudent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
