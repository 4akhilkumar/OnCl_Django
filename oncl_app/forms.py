from oncl_app.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class PositionForm(forms.Form):
    position = forms.CharField()

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class StaffsForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = ('gender','phone','address','branch','qualification','designation','git_link','website_link','linkedin_link','orcid_link','researcher_link','gscholar_link','microsoft_academic_link','bio','profile_pic')

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('gender','phone','address','branch','git_link','website_link','linkedin_link','bio','profile_pic') 

class MyfileUploadForm(forms.Form):
    book_id = forms.CharField(widget=forms.TextInput())
    book_name = forms.CharField(widget=forms.TextInput())
    book_author = forms.CharField(widget=forms.TextInput())
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
    session_pub_date = forms.CharField(widget=forms.TextInput())
    session_desc = forms.CharField(widget=forms.Textarea)
    session_tag1 = forms.CharField(widget=forms.TextInput())
    session_tag2 = forms.CharField(widget=forms.TextInput())
    session_tag3 = forms.CharField(widget=forms.TextInput())
    session_tag4 = forms.CharField(widget=forms.TextInput())
    session_pic = forms.FileField(widget=forms.FileInput())
    session_file = forms.FileField(widget=forms.FileInput())