from django.db import models
from django.contrib.auth.models import User

# Note: If migrations didn't detected then use this command -> py manage.py makemigrations app_name

# Create your models here.
class PCS_Cloud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course_name = models.CharField(max_length=200)
    topics = models.TextField(max_length=200, null=True, blank=True)
    url = models.TextField(max_length=200, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    faculty_name = models.CharField(max_length=200)
    faculty_email = models.CharField(max_length=200)
    faculty_phno = models.CharField(max_length=200)

    def __str__(self):
        return self.course_name
    
    class Meta:
        order_with_respect_to = 'user'

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
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
    branch_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()