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
        fields = ('gender','address',)

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('branch','gender','address','phone','git_link','website_link','linkedin_link','twitter_link','bio') 

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