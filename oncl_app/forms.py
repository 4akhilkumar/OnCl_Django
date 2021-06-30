from oncl_app.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class PositionForm(forms.Form):
    position = forms.CharField()

class BranchForm(forms.Form):
    model = Branches
    branch = forms.ChoiceField(choices = BRANCH_CHOICES)
    fields = ['branch']

class SemesterForm(forms.Form):
    SEM_MODE = (
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    )
    model = Semester
    semester_mode = forms.ChoiceField(choices = SEM_MODE)
    branch = forms.ChoiceField(choices = BRANCH_CHOICES)
    fields = ['semester_mode', 'branch', 'semester_start_year', 'semester_end_year']

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class StaffsForm(forms.ModelForm):
    class Meta:
        model = Staffs
        blood_group = forms.ChoiceField(choices = BLOOD_GROUP_CHOICES)
        mother_tounge = forms.ChoiceField(choices = MOTHER_TOUNGE_CHOICES)
        branch = forms.ChoiceField(choices = BRANCH_CHOICES)
        fields = ('gender','father_name','father_occ','father_phone','mother_name','mother_tounge','dob','blood_group','phone','dno_sn','zip_code','city_name','state_name','country_name','profile_pic','branch','qualification','designation')

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        blood_group = forms.ChoiceField(choices = BLOOD_GROUP_CHOICES)
        mother_tounge = forms.ChoiceField(choices = MOTHER_TOUNGE_CHOICES)
        branch = forms.ChoiceField(choices = BRANCH_CHOICES)
        fields = ['gender','father_name','father_occ','father_phone','mother_name','mother_tounge','dob','blood_group','phone','dno_sn','zip_code','city_name','state_name','country_name','profile_pic','branch'] 

class BookUploadForm(forms.Form):
    book_id = forms.CharField(widget=forms.TextInput())
    book_name = forms.CharField(widget=forms.TextInput())
    book_author = forms.CharField(widget=forms.TextInput())
    book_author_uid = forms.CharField(widget=forms.TextInput())
    book_pub_date = forms.CharField(widget=forms.TextInput())
    book_desc = forms.CharField(widget=forms.Textarea)
    book_tag1 = forms.CharField(widget=forms.TextInput())
    book_tag2 = forms.CharField(widget=forms.TextInput())
    book_tag3 = forms.CharField(widget=forms.TextInput())
    book_tag4 = forms.CharField(widget=forms.TextInput())
    book_pic = forms.FileField(widget=forms.FileInput())
    book_file = forms.FileField(widget=forms.FileInput())

class SessionUploadForm(forms.Form):
    session_id = forms.CharField(widget=forms.TextInput())
    session_name = forms.CharField(widget=forms.TextInput())
    session_author = forms.CharField(widget=forms.TextInput())
    session_author_uid = forms.CharField(widget=forms.TextInput())
    session_pub_date = forms.CharField(widget=forms.TextInput())
    session_desc = forms.CharField(widget=forms.Textarea)
    session_tag1 = forms.CharField(widget=forms.TextInput())
    session_tag2 = forms.CharField(widget=forms.TextInput())
    session_tag3 = forms.CharField(widget=forms.TextInput())
    session_tag4 = forms.CharField(widget=forms.TextInput())
    session_pic = forms.FileField(widget=forms.FileInput())
    session_file = forms.FileField(widget=forms.FileInput())
