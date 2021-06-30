from django.db.models import query
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django import template
import json
import datetime as pydt
import requests
import csv
import pandas as pd

from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core import mail

from django.views.generic import TemplateView
# Imports for Reordering Feature
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse

from django.views.decorators.csrf import csrf_exempt

from django.db import transaction

from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def te_page(request):
    return render(request, 'oncl_app/password_reset/password_reset_email.html')

def home_page(request):
    return render(request,'oncl_app/home.html')

def terms_of_service_page(request):
    return render(request,'oncl_app/footer_content_pages/legal/Terms of Service.html')

def privacy_policy_page(request):
    return render(request,'oncl_app/footer_content_pages/legal/Privacy Policy.html')

def cookies_policy_page(request):
    return render(request,'oncl_app/footer_content_pages/legal/Cookies Policy.html')

def GDPR_privacy_policy_page(request):
    return render(request,'oncl_app/footer_content_pages/legal/GDPR Privacy Policy.html')

def feedback_page(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            context = {
                'email':from_email, 'subject': subject, 'name':name, 'message':message,
            }
            template = render_to_string('oncl_app/feedback/admin_feedback_sent.html', context)
            body = render_to_string('oncl_app/feedback/user_mail.html', context)
            try:
                send_mail(subject, template, from_email, [settings.EMAIL_HOST_USER], html_message=template)
                send_mail('Thank you, For your feedback!', body, settings.EMAIL_HOST_USER, [from_email], html_message=body)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "oncl_app/feedback/feedback.html", {'form': form})

def successView(request):
        return render(request,'oncl_app/feedback/feedback_sent.html')

@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        current_email = request.POST.get('email')
        check_email = User.objects.filter(email=current_email).exists()
        if not check_email:
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                group = Group.objects.get(name='Student')
                user.groups.add(group)

                context = {'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name}
                template = render_to_string('oncl_app/login_register/register_mail.html', context)
                send_mail(first_name + ', welcome to your new OnCl Account', template, settings.EMAIL_HOST_USER, [email], html_message=template)				
                
                messages.success(request, 'Hey ' + username + '! Your Account is Created Succesfully!')
                return redirect('login')
        else:
            messages.warning(request, 'Email Already Exist!')
    context = {'form':form}
    return render(request, 'oncl_app/login_register/register.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        ip_addr = request.META['HTTP_X_FORWARDED_FOR']
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        location = request.POST.get('location')

        user = authenticate(request, username=username, password=password)

        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6LeJoakaAAAAACuq-D-kikqlQezY0ct5bs-OG6_b"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response=requests.post(url=cap_url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)

        if cap_json['success']==False:
            messages.error(request,"Invalid Captcha Try Again!")
            # return render(request,"oncl_app/login_register/recaptcha_message.html")
            return redirect('login')
        else:
            # messages.success(request, "Recaptcha Verified.")
            pass
        
        # if latitude == '5' and longitude == '5':
        #     messages.warning(request, 'You must enable your GPS inorder to login.')
        #     return redirect('login')

        # if location == '0':
        #     messages.warning(request, 'You must enable your GPS inorder to login.')
        #     return redirect('login')

        user_name = username
        save_login_details(request, user_name, ip_addr)

        if user is not None:
            login(request, user)
            messages.success(request, 'You Logged In Successfully.')
            template = render_to_string('oncl_app/login_register/login_mail.html', {'email':request.user.email, 'ip_addr':ip_addr, 'latitude':latitude, 'longitude':longitude})
            send_mail('OnCl Account Login Alert', template, settings.EMAIL_HOST_USER, [request.user.email], html_message=template)
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Student':
                return redirect('student_dashboard')
            elif group == 'Faculty':
                return redirect('faculty_dashboard')
            else:
                return redirect('admin_dashboard')

        else:
            messages.warning(request, 'Username or Password is Incorrect!')

    context = {}
    return render(request, 'oncl_app/login_register/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request,"You have logged out!")
    return redirect('login')

import re
import httpagentparser
def save_login_details(request, user_name, ip_addr):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']

    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]

    uid = User.objects.get(username=user_name)
    try:
        sld = user_login_details(ip_addr=ip_addr, user=uid, os_details=OS_Details, browser_details=browser)
        sld.save()
    except:
        return #

@unauthenticated_user
def dashboard_page(request):
    username = request.user.get_username()
    return #

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def dashboard_student_page(request):
    username = request.user.get_username()
    count_Task = Task.objects.filter(user=request.user.id).count()
    return render(request, 'oncl_app/dashboard_student.html', {'username':username, 'count_Task':count_Task,})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Faculty'])
def dashboard_faculty_page(request):
    username = request.user.get_username()
    count_Task = Task.objects.filter(user=request.user.id).count()
    return render(request, 'oncl_app/dashboard_faculty.html', {'username':username, 'count_Task':count_Task,})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def dashboard_admin_page(request):
    username = request.user.get_username()
    count_LeaveReportStudent = LeaveReportStudent.objects.all().count()
    count_LeaveReportStaff = LeaveReportStaff.objects.all().count()
    count_Task = Task.objects.filter(user=request.user.id).count()

    context = {
        'username':username,
        'count_LeaveReportStudent':count_LeaveReportStudent,
        'count_LeaveReportStaff':count_LeaveReportStaff,
        'count_Task':count_Task,
    }
    return render(request, 'oncl_app/dashboard_admin.html', context)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        query = self.request.GET.get('search-area') or ''
        if query:
            context['tasks'] = context['tasks'].filter(Q(title__contains=query) | Q(description__contains=query))
        context['search_input'] = query

        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

@login_required(login_url='login')
def audio_page(request):
    return render(request,'oncl_app/study_session_audio.html')

def unauthorized_access(request):
    return render(request, 'oncl_app/page_not_found/page-401.html')

def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'oncl_app/page_not_found/page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template( 'oncl_app/page_not_found/page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_semester(request):
    semester_form = SemesterForm()
    context = {
        "semester_form":semester_form
    }
    return render(request, "oncl_app/admin_templates/semester_templates/add_semester.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_semester_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_branch')
    else:
        semester_mode = request.POST.get('semester_mode')
        semester_start_year = request.POST.get('semester_start_year')
        semester_end_year = request.POST.get('semester_end_year')
        branch = request.POST.get('branch')

        try:
            semesteryear = Semester(semester_mode=semester_mode,semester_start_year=semester_start_year, semester_end_year=semester_end_year,branch=branch)
            semesteryear.save()
            messages.success(request, "Semester Planned Successfully.")
            return redirect("manage_semester")
        except:
            messages.error(request, "Failed to Plan Semester!")
            return redirect("add_semester")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_semester(request, semester_id):
    semester_year = Semester.objects.get(id=semester_id)
    semester_form = SemesterForm()
    context = {
        "semester_year": semester_year,
        "semester_form":semester_form,
    }
    return render(request, "oncl_app/admin_templates/semester_templates/edit_semester.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_semester_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_semester')
    else:
        semester_id = request.POST.get('semester_id')
        semester_mode = request.POST.get('semester_mode')
        semester_start_year = request.POST.get('semester_start_year')
        semester_end_year = request.POST.get('semester_end_year')
        branch = request.POST.get('branch')

        try:
            semester_year = Semester.objects.get(id=semester_id)
            semester_year.semester_mode = semester_mode
            semester_year.semester_start_year = semester_start_year
            semester_year.semester_end_year = semester_end_year
            semester_year.branch = branch
            semester_year.save()

            messages.success(request, "Semester Re-Planned Successfully.")
            return redirect('manage_semester')
        except:
            messages.error(request, "Failed to Re-Plan Semester!.")
            return redirect('/edit_semester/'+semester_id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_semester(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    try:
        semester.delete()
        messages.success(request, "Semester Deleted Successfully.")
        return redirect('manage_semester')
    except:
        messages.error(request, "Failed to Delete Semester!")
        return redirect('manage_semester')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def manage_semester(request):
    semester_years = Semester.objects.order_by('semester_start_year')
    context = {
        "semester_years": semester_years
    }
    return render(request, "oncl_app/admin_templates/semester_templates/manage_semester.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_branch(request):
    branches = Branches.objects.all()
    context = {
        "branches":branches
    }
    return render(request, "oncl_app/admin_templates/branch_templates/add_branch.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_branch_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_branch')
    else:
        branch = request.POST.get('branch')
        try:
            branch_model = Branches(branch=branch)
            branch_model.save()
            messages.success(request, "Branch Added Successfully.")
            return redirect('manage_branch')
        except:
            messages.error(request, "Failed to Add Branch!")
            return redirect('add_branch')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def manage_branch(request):
    branches = Branches.objects.all()
    context = {
        "branches": branches
    }
    return render(request, 'oncl_app/admin_templates/branch_templates/manage_branch.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_branch(request, branch_id):
    branch = Branches.objects.get(id=branch_id)
    branches = Branches.objects.all()
    context = {
        "branch": branch,
        "branches":branches,
        "id": branch_id
    }
    return render(request, 'oncl_app/admin_templates/branch_templates/edit_branch.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_branch_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        branch_id = request.POST.get('branch_id')
        branch_name = request.POST.get('branch')

        try:
            branch = Branches.objects.get(id=branch_id)
            branch.branch = branch_name
            branch.save()

            messages.success(request, "Branch Updated Successfully!")
            return redirect('manage_branch')
        except:
            messages.error(request, "Failed to Update Branch!")
            return redirect('/edit_branch/'+branch_id+'/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_branch(request, branch_id):
    branch = Branches.objects.get(id=branch_id)
    try:
        branch.delete()
        messages.success(request, "Branch Deleted Successfully.")
        return redirect('manage_branch')
    except:
        messages.error(request, "Failed to Delete Branch!")
        return redirect('manage_branch')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_subject(request):
    student_form = StudentsForm()
    staffs = User.objects.filter(groups='2')
    context = {
        "student_form": student_form,
        "staffs": staffs
    }
    return render(request, 'oncl_app/admin_templates/subject_templates/add_subject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')
        branch_id = request.POST.get('branch')
        staff_id = request.POST.get('staff')
        staff = User.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name, branch=branch_id, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully.")
            return redirect('manage_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'oncl_app/admin_templates/subject_templates/manage_subject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    student_form = StudentsForm()
    staffs = User.objects.filter(groups='2')
    context = {
        "subject": subject,
        "staffs": staffs,
        "id": subject_id,
        "student_form": student_form,
    }
    return render(request, 'oncl_app/admin_templates/subject_templates/edit_subject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        branch = request.POST.get('branch')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            subject.branch = branch
            staff = User.objects.get(id=staff_id)
            subject.staff_id = staff
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            return redirect('manage_subject')

        except:
            messages.error(request, "Failed to Update Subject!")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject!")
        return redirect('manage_subject')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_staff(request):
    form = CreateUserForm()
    staff_form = StaffsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        staff_form = StaffsForm(request.POST,request.FILES)

        if form.is_valid() and staff_form.is_valid():
            user = form.save()
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username = username, password = password)

            group = Group.objects.get(name='Faculty')
            user.groups.add(group)

            return redirect('manage_staff')
        else:
            form = CreateUserForm()
            staff_form = StaffsForm()

    context = {'form':form, 'staff_form':staff_form}        
    return render(request, "oncl_app/admin_templates/faculty_templates/add_faculty.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def manage_staff(request):
    staffs_all = Staffs.objects.all()
    page = request.GET.get('page', 1)
    
    paginator = Paginator(staffs_all, 11)
    try:
        staffs = paginator.page(page)
    except PageNotAnInteger:
        staffs = paginator.page(1) 
    except EmptyPage:
        staffs = paginator.page(paginator.num_pages)

    context = {
        "staffs": staffs,
        "staffs_all": staffs_all
    }
    return render(request, "oncl_app/admin_templates/faculty_templates/manage_faculty.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_staff(request, staff_id):
    staff = Staffs.objects.get(user=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "oncl_app/admin_templates/faculty_templates/edit_faculty.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student'])
def view_staff(request, staff_id):
    staff = Staffs.objects.get(user=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "oncl_app/profile_templates/admin_faculty_view_profile.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        qualification = request.POST.get('qualification')
        branch = request.POST.get('branch')
        desgination = request.POST.get('desgination')
        address = request.POST.get('address')

        if 'profile_pic' in request.FILES:
            print("YES")
            profile_pic = request.FILES['profile_pic']
            print("If part",profile_pic)
        else:
            print("Else Part")
            profile_pic = 'avatar.webp'
            print("Else part",profile_pic)
            print("NO")

        try:
            # INSERTING into User Model
            user = User.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(user=staff_id)
            staff_model.gender = gender
            staff_model.phone = phone
            staff_model.branch = branch
            staff_model.desgination = desgination
            staff_model.address = address
            staff_model.qualification = qualification
            if profile_pic == 'avatar.webp':
                pass
            else:
                staff_model.profile_pic = profile_pic
            staff_model.save()

            # return redirect('/edit_staff/'+staff_id)
            messages.success(request, "Faculty Info. Updated Successfully.")
            return redirect('manage_staff')

        except:
            messages.error(request, "Failed to Update Faculty Info.!")
            return redirect('/edit_staff/'+staff_id+"/")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_staff(request, staff_id):
    staff = Staffs.objects.get(user=staff_id)
    try:
        staff.delete()
        staff.user.delete()
        messages.info(request, "Faculty Record Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Faculty Record!")
        return redirect('manage_staff')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_student(request):
    form = CreateUserForm()
    student_form = StudentsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        student_form = StudentsForm(request.POST,request.FILES)

        if form.is_valid() and student_form.is_valid():
            user = form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username = username, password = password)

            group = Group.objects.get(name='Student')
            user.groups.add(group)

            return redirect('manage_student')
        else:
            form = CreateUserForm()
            student_form = StudentsForm()

    context = {'form':form, 'student_form':student_form}        
    return render(request, "oncl_app/admin_templates/student_templates/add_student.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def manage_student(request):
    students_all = Students.objects.all()
    page = request.GET.get('page', 1)
    
    paginator = Paginator(students_all, 11)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context = {
        "students": students,
        "students_all": students_all
    }
    return render(request, "oncl_app/admin_templates/student_templates/manage_student.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_student(request, student_id):
    student = Students.objects.get(user=student_id)
    student_form = StudentsForm()
    context = {
        "student": student,
        "id": student_id,
        "student_form":student_form,
    }
    return render(request, "oncl_app/admin_templates/student_templates/edit_student.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get('student_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        father_name = request.POST.get('father_name')
        father_occ = request.POST.get('father_occ')
        father_phone = request.POST.get('father_phone')
        mother_name = request.POST.get('mother_name')
        mother_tounge = request.POST.get('mother_tounge')
        dob = request.POST.get('dob')
        blood_group = request.POST.get('blood_group')
        phone = request.POST.get('phone')
        dno_sn = request.POST.get('dno_sn')
        zip_code = request.POST.get('zip_code')
        city_name = request.POST.get('city_name')
        state_name = request.POST.get('state_name')
        country_name = request.POST.get('country_name')
        branch = Branches.objects.get(id=branch)
        branch = request.POST.get('branch')

        if 'profile_pic' in request.FILES:
            print("YES")
            profile_pic = request.FILES['profile_pic']
            print("If part",profile_pic)
        else:
            print("Else Part")
            profile_pic = 'avatar.webp'
            print("Else part",profile_pic)
            print("NO")

        try:
            # INSERTING into User Model
            user = User.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Students Model
            student_model = Students.objects.get(user=student_id)
            student_model.gender = gender
            student_model.father_name = father_name
            student_model.father_occ = father_occ
            student_model.father_phone = father_phone
            student_model.mother_name = mother_name
            student_model.mother_tounge = mother_tounge
            student_model.dob = dob
            student_model.blood_group = blood_group
            student_model.phone = phone
            student_model.dno_sn = dno_sn
            student_model.zip_code = zip_code
            student_model.city_name = city_name
            student_model.state_name = state_name
            student_model.country_name = country_name
            student_model.branch = branch            

            if profile_pic == 'avatar.webp':
                pass
            else:
                student_model.profile_pic = profile_pic
            student_model.save()

            messages.success(request, "Student Info. Updated Successfully.")
            return redirect('manage_student')
        
        except:
            messages.error(request, "Failed to Update Student Info.!")
            return redirect('/edit_student/'+student_id+"/")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def view_student(request, student_id):
    student = Students.objects.get(user=student_id)
    sld = user_login_details.objects.filter(user=student_id)
    ssp = Student_Social_Profile.objects.filter(user=student_id)
    print(sld)
    context = {
        "student": student,
        "id": student_id,
        "sld":sld,
        "ssp":ssp,
    }
    return render(request, "oncl_app/profile_templates/student_profile.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_student(request, student_id):
    student = Students.objects.get(user=student_id)
    try:
        student.delete()
        student.user.delete()
        messages.info(request, "Student Record Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student Record!")
        return redirect('manage_student')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def add_announcement(request):
    username = request.user.get_username()
    staffs = User.objects.filter(groups='2')
    context={
            'username':username,
            'staffs':staffs,
        }
    return render(request, "oncl_app/admin_templates/announcements_templates/add_announcement.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def add_announcement_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_announcement')
    else:
        announcement = request.POST.get('announcement')
        sub_an = request.POST.get('sub_an')
        an_by = request.POST.get('an_by')
        an_user = request.POST.get('an_user')
        if 'an_image' in request.FILES:
            print("YES")
            an_image = request.FILES['an_image']
            print(an_image)
        else:
            an_image = False
            print("No")
            print(an_image)
 
        try:
            announcement_model = Announcements_news(what_an=announcement,sub_an=sub_an,an_by=an_by,an_user=an_user,an_image=an_image)
            announcement_model.save()
            messages.success(request, "Announcement Made Successfully.")
            return redirect('manage_announcement')
        except:
            messages.error(request, "Failed to Make Announcement!")
            return redirect('add_announcement')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def manage_announcement(request):
    announcements_all = Announcements_news.objects.order_by('-created_at')
    page = request.GET.get('page', 1)
    
    paginator = Paginator(announcements_all, 11)
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)

    context = {
        "announcements": announcements,
        "announcements_all":announcements_all,
    }
    return render(request, 'oncl_app/admin_templates/announcements_templates/manage_announcements.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def edit_announcement(request, announcement_id):
    announcement = Announcements_news.objects.get(id=announcement_id)
    context = {
        "announcement": announcement,
        "id": announcement_id
    }
    return render(request, 'oncl_app/admin_templates/announcements_templates/edit_announcement.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def edit_announcement_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        announcement_id = request.POST.get('announcement_id')
        sub_an = request.POST.get('sub_an')
        what_an = request.POST.get('announcement')
        an_by = request.POST.get('an_by')
        an_user = request.POST.get('an_user')
        if 'an_image' in request.FILES:
            print("YES")
            an_image = request.FILES['an_image']
            print(an_image)
        else:
            an_image = False
            print("No")
            print(an_image)

        try:
            announcement = Announcements_news.objects.get(id=announcement_id)
            announcement.what_an = what_an
            announcement.sub_an = sub_an
            announcement.an_by = an_by
            announcement.an_user = an_user
            if an_image == False:
                pass
            else:
                announcement.an_image = an_image
            announcement.save()

            messages.success(request, "Announcement Updated Successfully!")
            return redirect('manage_announcement')

        except:
            messages.error(request, "Failed to Update Announcement!")
            return redirect('/edit_announcement/'+announcement_id+'/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def delete_announcement(request, announcement_id):
    announcement = Announcements_news.objects.get(id=announcement_id)
    try:
        announcement.delete()
        messages.info(request, "Announcement Deleted Successfully.")
        return redirect('manage_announcement')
    except:
        messages.error(request, "Failed to Delete Announcement!")
        return redirect('manage_announcement')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Faculty'])
def faculty_profile(request):
    username = request.user.get_username()
    user = User.objects.get(id=request.user.id)
    staff = Staffs.objects.get(user=user)
    context={
            'username':username, 'staff':staff, "user": user
        }
    return render(request, 'oncl_app/profile_templates/faculty_profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def student_profile(request):
    username = request.user.get_username()
    user = User.objects.get(id=request.user.id)
    student = Students.objects.get(user=user)
    sld = user_login_details.objects.filter(user=user)
    ssp = Student_Social_Profile.objects.filter(user=request.user.id)
    print(ssp, sld)
    context = {
            'username':username,
            'student':student, 
            "user": user, 
            "sld":sld,
            "ssp":ssp
        }
    return render(request, 'oncl_app/profile_templates/student_profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Librarian','Faculty'])
def upload(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST,request.FILES)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            book_name = form.cleaned_data['book_name']
            book_author = form.cleaned_data['book_author']
            book_author_uid = form.cleaned_data['book_author_uid']
            book_desc = form.cleaned_data['book_desc']
            book_pub_date = form.cleaned_data['book_pub_date']
            book_pic = form.cleaned_data['book_pic']
            book_file = form.cleaned_data['book_file']
            book_tag1 = form.cleaned_data['book_tag1']
            book_tag2 = form.cleaned_data['book_tag2']
            book_tag3 = form.cleaned_data['book_tag3']
            book_tag4 = form.cleaned_data['book_tag4']

            E_Books(book_id = book_id,
                        book_name = book_name, 
                        book_author = book_author, 
                        book_author_uid = book_author_uid,
                        book_desc = book_desc,
                        book_pub_date = book_pub_date,
                        book_pic = book_pic,
                        book_file = book_file,
                        book_tag1 = book_tag1,
                        book_tag2 = book_tag2,
                        book_tag3 = book_tag3,
                        book_tag4 = book_tag4).save()
            messages.success(request, "E-Book Uploaded Successfully.")
            return redirect('view_book')
        else:
            messages.error(request, "Failed to Uploaded E-Book!")
            return redirect('upload_book')
    else:
        context={
            'form': BookUploadForm()
        }
        return render(request, "oncl_app/E-Library/upload_book.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def view_books(request):
    all_data_all = E_Books.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(all_data_all, 21)
    try:
        all_data = paginator.page(page)
    except PageNotAnInteger:
        all_data = paginator.page(1)
    except EmptyPage:
        all_data = paginator.page(paginator.num_pages)

    context = {
        'data':all_data,
        'all_data_all':all_data_all,
    }
    return render(request,'oncl_app/E-Library/view_books.html', context)


def edit_book(request, book_id):
    e_book = E_Books.objects.get(id=book_id)
    context = {
        "e_book": e_book,
        "id": book_id
    }
    return render(request, 'oncl_app/E-Library/edit_book.html', context)

def edit_book_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        main_book_id = request.POST.get('main_book_id')
        book_id = request.POST.get('book_id')
        book_name = request.POST.get('book_name')
        book_author = request.POST.get('book_author')
        book_pub_date = request.POST.get('book_pub_date')
        book_desc = request.POST.get('book_desc')
        book_tag1 = request.POST.get('book_tag1')
        book_tag2 = request.POST.get('book_tag2')
        book_tag3 = request.POST.get('book_tag3')
        book_tag4 = request.POST.get('book_tag4')
        
        if 'book_pic' in request.FILES:
            print("YES")
            book_pic = request.FILES['book_pic']
            print(book_pic)
        else:
            book_pic = False
            print("No")
            print(book_pic)
        if 'book_file' in request.FILES:
            print("YES")
            book_file = request.FILES['book_file']
            print(book_file)
        else:
            book_file = False
            print("No")
            print(book_file)

        try:
            e_book = E_Books.objects.get(id=main_book_id)
            e_book.book_id = book_id
            e_book.book_name = book_name
            e_book.book_author = book_author
            e_book.book_pub_date = book_pub_date
            e_book.book_desc = book_desc
            e_book.book_tag1 = book_tag1
            e_book.book_tag2 = book_tag2
            e_book.book_tag3 = book_tag3
            e_book.book_tag4 = book_tag4
            
            if book_pic == False:
                pass
            else:
                e_book.book_pic = book_pic
            if book_file == False:
                pass
            else:
                e_book.book_file = book_file
            e_book.save()

            messages.success(request, "Book Info. Updated Successfully.")
            return redirect('view_book')

        except:
            messages.error(request, "Failed to Update Book Info.!")
            return redirect('/edit_book/'+main_book_id+'/')

def delete_book(request, book_id):
    e_book = E_Books.objects.get(id=book_id)
    try:
        e_book.delete()
        messages.info(request, "E-Book Deleted Successfully.")
        return redirect('view_book')
    except:
        messages.error(request, "Failed to Delete E-Book!")
        return redirect('view_book')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def search(request):
    if request.method == 'POST':
        now = pydt.datetime.now()
        query = request.POST['search']
        books = E_Books.objects.filter(
            Q(book_id__contains=query) | Q(book_name__contains=query) | 
            Q(book_author__contains=query) | Q(book_desc__contains=query) | 
            Q(book_pub_date__contains=query) | Q(book_tag1__contains=query) | 
            Q(book_tag2__contains=query) | Q(book_tag3__contains=query) | 
            Q(book_tag4__contains=query))
        now1 = pydt.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/E-Library/search_books.html', {'books': books, 'cal_time':cal_time, 'query':query})
    else:
        all_data = E_Books.objects.all()
        context = {
            'data': all_data 
        }
        return render(request, 'oncl_app/E-Library/view_books.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def search_announcements(request):
    if request.method == 'POST':
        now = pydt.datetime.now()
        query = request.POST['search']
        announcements = Announcements_news.objects.filter(
            Q(sub_an__contains=query) | Q(what_an__contains=query) | Q(an_by__contains=query) | 
            Q(created_at__contains=query) | Q(updated_at__contains=query))
        now1 = pydt.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/admin_templates/announcements_templates/search_announcements.html', {'announcements': announcements, 'cal_time':cal_time})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def search_faculty(request):
    if request.method == 'POST':
        now = pydt.datetime.now()
        query = request.POST['search']
        staff = Staffs.objects.filter(
             Q(user__first_name__contains=query) | Q(user__last_name__contains=query) |
            Q(user__email__contains=query) | Q(user__username__contains=query) |
            Q(gender__contains=query) | Q(address__contains=query))

        now1 = pydt.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/admin_templates/faculty_templates/search_faculty.html', {'staffs': staff, 'cal_time':cal_time, 'query':query})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def search_student(request):
    if request.method == 'POST':
        now = pydt.datetime.now()
        query = request.POST['search']
        student = Students.objects.filter(
            Q(user__first_name__contains=query) | Q(user__last_name__contains=query) |
            Q(user__email__contains=query) | Q(user__username__contains=query) |
            Q(gender__contains=query) | Q(father_name__contains=query) |
            Q(father_occ__contains=query) | Q(father_phone__contains=query) |
            Q(mother_name__contains=query) | Q(mother_tounge__contains=query) |
            Q(dob__contains=query) | Q(blood_group__contains=query) |
            Q(phone__contains=query) | Q(dno_sn__contains=query) |
            Q(zip_code__contains=query) | Q(city_name__contains=query) |
            Q(state_name__contains=query) | Q(country_name__contains=query) |
            Q(branch__contains=query))

        now1 = pydt.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/admin_templates/student_templates/search_student.html', {'students': student, 'cal_time':cal_time, 'query':query})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def upload_session(request):
    if request.method == 'POST':
        form = SessionUploadForm(request.POST,request.FILES)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            session_name = form.cleaned_data['session_name']
            session_author = form.cleaned_data['session_author']
            session_author_uid = form.cleaned_data['session_author_uid']
            session_desc = form.cleaned_data['session_desc']
            session_pub_date = form.cleaned_data['session_pub_date']
            session_pic = form.cleaned_data['session_pic']
            session_file = form.cleaned_data['session_file']
            session_tag1 = form.cleaned_data['session_tag1']
            session_tag2 = form.cleaned_data['session_tag2']
            session_tag3 = form.cleaned_data['session_tag3']
            session_tag4 = form.cleaned_data['session_tag4']

            PCS_Cloud(session_id = session_id,
                        session_name = session_name, 
                        session_author = session_author,
                        session_author_uid = session_author_uid,
                        session_desc = session_desc,
                        session_pub_date = session_pub_date,
                        session_pic = session_pic,
                        session_file = session_file,
                        session_tag1 = session_tag1,
                        session_tag2 = session_tag2,
                        session_tag3 = session_tag3,
                        session_tag4 = session_tag4).save()
            messages.success(request, "Session Info. Uploaded Successfully.")
            return redirect('view_session')
        else:
            messages.error(request, "Failed to Upload Session Info.!")
            return redirect('upload_session')
    else:
        context={
            'form': SessionUploadForm()
        }
        return render(request, "oncl_app/PCS_Cloud/upload_session.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def view_session(request):
    all_data_all = PCS_Cloud.objects.all()

    page = request.GET.get('page', 1)    
    paginator = Paginator(all_data_all, 20)
    try:
        all_data = paginator.page(page)
    except PageNotAnInteger:
        all_data = paginator.page(1)
    except EmptyPage:
        all_data = paginator.page(paginator.num_pages)

    context = {
        'data':all_data,
        'all_data_all':all_data_all,
    }
    return render(request,'oncl_app/PCS_Cloud/view_sessions.html', context)

def edit_session(request, session_id):
    session = PCS_Cloud.objects.get(id=session_id)
    context = {
        "session": session,
        "id": session_id
    }
    return render(request, 'oncl_app/PCS_Cloud/edit_session.html', context)

def view_each_session(request, session_id):
    session = PCS_Cloud.objects.get(id=session_id)
    context = {
        "session": session,
        "id": session_id
    }
    return render(request, 'oncl_app/PCS_Cloud/view_each_session.html', context)

def edit_session_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        main_session_id = request.POST.get('main_session_id')
        session_id = request.POST.get('session_id')
        session_name = request.POST.get('session_name')
        session_author = request.POST.get('session_author')
        session_pub_date = request.POST.get('session_pub_date')
        session_desc = request.POST.get('session_desc')
        session_tag1 = request.POST.get('session_tag1')
        session_tag2 = request.POST.get('session_tag2')
        session_tag3 = request.POST.get('session_tag3')
        session_tag4 = request.POST.get('session_tag4')
        
        if 'session_pic' in request.FILES:
            print("YES")
            session_pic = request.FILES['session_pic']
            print(session_pic)
        else:
            session_pic = False
            print("No")
            print(session_pic)
        if 'session_file' in request.FILES:
            print("YES")
            session_file = request.FILES['session_file']
            print(session_file)
        else:
            session_file = False
            print("No")
            print(session_file)

        try:
            session = PCS_Cloud.objects.get(id=main_session_id)
            session.session_id = session_id
            session.session_name = session_name
            session.session_author = session_author
            session.session_pub_date = session_pub_date
            session.session_desc = session_desc
            session.session_tag1 = session_tag1
            session.session_tag2 = session_tag2
            session.session_tag3 = session_tag3
            session.session_tag4 = session_tag4
            
            if session_pic == False:
                pass
            else:
                session.session_pic = session_pic
            if session_file == False:
                pass
            else:
                session.session_file = session_file
            session.save()

            messages.success(request, "Session Info. Updated Successfully.")
            return redirect('view_session')

        except:
            messages.error(request, "Failed to Update Session Info.!")
            return redirect('/edit_session/'+main_session_id+'/')

def delete_session(request, session_id):
    session = PCS_Cloud.objects.get(id=session_id)
    try:
        session.delete()
        messages.info(request, "Session Deleted Successfully.")
        return redirect('view_session')
    except:
        messages.error(request, "Failed to Delete Session!")
        return redirect('view_session')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def search_session(request):
    if request.method == 'POST':
        now = pydt.datetime.now()
        query = request.POST['search']
        
        sessions = PCS_Cloud.objects.filter(
            Q(session_id__contains=query) | Q(session_name__contains=query) | 
            Q(session_author__contains=query) | Q(session_desc__contains=query) | 
            Q(session_pub_date__contains=query) | Q(session_tag1__contains=query) | 
            Q(session_tag2__contains=query) | Q(session_tag3__contains=query) | 
            Q(session_tag4__contains=query))
        now1 = pydt.datetime.now()
        cal_time = (now1 - now).total_seconds()

        context = {
            'sessions': sessions,
            'cal_time':cal_time,
        }
        return render(request, 'oncl_app/PCS_Cloud/search_sessions.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def aca_stats(request):
    staff_count = Staffs.objects.all().count()
    student_count = Students.objects.all().count()
    student_leave_count = LeaveReportStudent.objects.all().count()
    staff_leave_count = LeaveReportStaff.objects.all().count()
    branch_all = Branches.objects.all()
    branch_list = []
    subject_count_list = []
    male_count = Students.objects.filter(gender="Male").count()
    female_count = Students.objects.filter(gender="Female").count()

    for branch in branch_all:
        subjects = Subjects.objects.filter(branch=branch.branch).count()
        branch_list.append(branch.branch)
        subject_count_list.append(subjects)
        print(subjects)
        print(subject_count_list)

    staff_count_15 = staff_count*15

    staffs = Staffs.objects.all()
    values2=[]
    for i in branch_list:
        cc=0
        for j in staffs:
            if(i==j.branch):
                cc+=1
        values2.append(cc)

    students=Students.objects.all()
    values=[]
    for i in branch_list:
        c=0
        for j in students:
            if(i==j.branch):
                c+=1
        values.append(c)

    context = {
        "staff_count":staff_count,
        "student_count":student_count,
        "branch_list":branch_list,
        "subject_count_list":subject_count_list,
        "male_count":male_count,
        "female_count":female_count,
        "staff_count_15":staff_count_15,
        "values":values,
        "values2":values2,
        "student_leave_count":student_leave_count,
        "staff_leave_count":staff_leave_count
    }
    return render(request, 'oncl_app/admin_templates/aca_stats.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def student_apply_leave(request):
    student_obj = Students.objects.get(user=request.user.id) 
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'oncl_app/student_templates/student_apply_leave.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(user=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'oncl_app/admin_templates/permission_templates/student_leave_view.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def student_leave_undo(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 0 
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'oncl_app/admin_templates/permission_templates/staff_leave_view.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def staff_leave_undo(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 0
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Faculty'])
def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(user=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "oncl_app/faculty_templates/staff_apply_leave_template.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Faculty'])
def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(user=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def timetable(request):
    return render(request, 'oncl_app/timetable.html')


RUN_URL = "https://api.hackerearth.com/v3/code/run/"

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def index(request):
    return render(request, 'oncl_app/index.html', {})

#From HackerEarth API
def runCode(request):
    if request.is_ajax():
        source = request.POST['source']
        lang = request.POST['lang']
        data = {
            'client_secret': '7bd75915143fdc69b470c84d9fd3d40a3fb40342' ,
            'async': 0,
            'source': source,
            'lang': lang,
            'time_limit': 5,
            'memory_limit': 262144,
        }
        if 'input' in request.POST:
            data['input'] = request.POST['input']
        r = requests.post(RUN_URL, data=data)
        return JsonResponse(r.json(), safe=False)
    else:
        return HttpResponseForbidden()

def exam_student(request):
    user = User.objects.get(id=request.user.id)
    student = Students.objects.get(user=user)
    branch = student.branch
    branch_id = Branches.objects.get(branch=branch)
    branch_id_ = branch_id.id
    subject_list = Subjects.objects.filter(branch_id=branch_id_)

    context = {
        "subject_list":subject_list,
        "student":student,
        "user":user
    }
    return render(request, 'oncl_app/exam_module/take_exam_subject.html', context)

def show_que(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('exam_student')
    else:
        subject_name = request.POST.get('subject_name')
        student_obj = Students.objects.get(user=request.user.id)
        e = Exam.objects.filter(student_id=student_obj).filter(exam_sub=subject_name)
        if e:
            return render(request, 'oncl_app/exam_module/already_submitted.html')
        else:
            subject = Subjects.objects.get(subject_name=subject_name)
            subject_id = subject.id
            que = Exam_ques.objects.filter(subject_id=subject_id)
            context = {
                "que":que,
                "subject_name":subject_name,
            }
            return render(request, 'oncl_app/exam_module/get_question.html', context)
        return redirect('dashboard')

def upload_answers(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('exam_student')
    else:
        student_obj = Students.objects.get(user=request.user.id)
        subject_name = request.POST.get('exam_sub')
        ans_file = request.FILES['ans_file']
        exam = Exam(student_id=student_obj,exam_sub=subject_name,ans_file=ans_file)
        exam.save()
        messages.success(request, "Your Submission is Taken.")
        return render(request, 'oncl_app/exam_module/submit_message.html')

def exam_evaluation(request):
    user = User.objects.get(id=request.user.id)
    staff = Staffs.objects.get(user=user)
    staff_id = staff.user.id
    subject_list = Subjects.objects.filter(staff_id=staff_id)

    context = {
        "subject_list":subject_list,
        "staff":staff
    }
    return render(request, 'oncl_app/exam_module/faculty_subject.html', context)

def view_student_exam(request):
    subject = request.POST.get("subject_name")
    student = Exam.objects.filter(exam_sub=subject)

    context = {
        "student":student,
    }
    return render(request, 'oncl_app/exam_module/view_exam.html', context)

def assign_marks(request, student_id):
    exam = Exam.objects.get(id=student_id)
    student = exam.student_id
    context = {
        "exam": exam,
        "id": student_id,
        "student":student
    }
    return render(request, 'oncl_app/exam_module/update_marks.html', context)  

def assign_marks_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        exam_id = request.POST.get('exam_id')
        marks = request.POST.get('marks')

        try:
            exam_model = Exam.objects.get(id=exam_id)
            exam_model.exam_marks = marks
            exam_model.save()

            messages.success(request, "Marks Assigned Successfully!")
            return redirect('exam_evaluation')

        except:
            messages.error(request, "Failed to Assign Marks!")
            return redirect('assign_marks')

def view_my_marks(request):
    student_obj = Students.objects.get(user=request.user.id) 
    exam = Exam.objects.filter(student_id=student_obj)
    context = {
            'exam':exam
    }
    return render(request, 'oncl_app/exam_module/view_my_marks.html', context)

def view_marks_admin(request):
    exam_info = Exam.objects.all()
    context = {
            'exam_info':exam_info
    }
    return render(request, 'oncl_app/exam_module/view_marks_admin.html', context)

def start_live_classroom(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    return render(request,"oncl_app/faculty_templates/start_live_classroom.html", {"subjects":subjects})

from datetime import datetime
from uuid import uuid4
def start_live_classroom_process(request):
    subject=request.POST.get("subject")

    subject_obj=Subjects.objects.get(id=subject)
    checks=OnlineClassRoom.objects.filter(subject=subject_obj,is_active=True).exists()
    if checks:
        data=OnlineClassRoom.objects.get(subject=subject_obj,is_active=True)
        room_pwd=data.room_pwd
        roomname=data.room_name
    else:
        room_pwd=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        roomname=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        staff_obj=Staffs.objects.get(user=request.user.id)
        onlineClass=OnlineClassRoom(room_name=roomname,room_pwd=room_pwd,subject=subject_obj,started_by=staff_obj,is_active=True)
        onlineClass.save()

    return render(request,"oncl_app/faculty_templates/live_class_room_start.html",{"username":request.user.username,"password":room_pwd,"roomid":roomname,"subject":subject_obj.subject_name})

def join_class_room(request,subject_id):
    subjects=Subjects.objects.filter(id=subject_id)
    if subjects.exists():
        subject_obj=Subjects.objects.get(id=subject_id)
        onlineclass=OnlineClassRoom.objects.get(subject=subject_id)
        return render(request,"oncl_app/student_templates/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})
    else:
        return HttpResponse("Subject Not Found")
        
def returnHtmlWidget(request):
    return render(request,"oncl_app/faculty_templates/widget.html")

def show_subject(request):
    user = User.objects.get(id=request.user.id)
    staff = Staffs.objects.get(user=user)
    staff_id = staff.user.id
    subject_list = Subjects.objects.filter(staff_id=staff_id)

    context = {
        "subject_list":subject_list,
        "staff":staff
    }
    return render(request, 'oncl_app/admin_templates/attendance_templates/fetch_student_subject.html', context)

def branch_students(request):
    user = User.objects.get(id=request.user.id)
    staff = Staffs.objects.get(user=user)
    branch = staff.branch
    students=Students.objects.filter(branch=branch)
    subject = request.POST.get('subject_name')
    attendance = AttendanceReportStudent.objects.filter(branch_id=branch)
    # date = date.today()
    context={
        'branch':branch,
        'students':students,
        'subject':subject,
        'attendance':attendance,
        # 'date':date
    }
    return render(request,"oncl_app/attendance/view_students.html",context)

def save_attendance(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        attend_status = request.POST.get('attend_status')
        branch = request.POST.get('branch')
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')

        ars = AttendanceReportStudent(student_id=student_id,branch_id=branch,subject=subject,attend_status=attend_status)
        ars.save()
        messages.success(request, "Attendance Saved Successfully.")
        return redirect('branch_students')

def student_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=student_info_record' + \
        str(pydt.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 
                    'Gender', 'Father Name', 'Father Occupation', 'Father Phone', 'Mother Name', 'Mother Tounge', 'Date of Birth',
                    'Blood Group', 'Phone', 'Door No.', 'Zip Code', 'City Name', 'State Name', 'Country', 'Branch', 'Last Login'])
    
    student = Students.objects.all()

    for i in student:
        writer.writerow([i.user.username, i.user.first_name, i.user.last_name, i.user.email,
                        i.gender, i.father_name, i.father_occ, i.father_phone, i.mother_name, i.mother_tounge,
                        i.dob, i.blood_group, i.phone, i.dno_sn, i.zip_code, i.city_name, i.state_name, i.country_name, i.branch, i.user.last_login])
    return response

def bulk_upload_students(request):
    return render(request, 'oncl_app/testing.html')

def bulk_upload_students_save(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['studentfile'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in student_user and str(row['Email']) not in student_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password=row['Password'],
                )
                Student=Group.objects.get(name='Student')
                if row['Group'] == 'Student':
                    Student.user_set.add(newuser)
                    newuser.groups.add(Student)

                student = Students.objects.bulk_create([
                    Students(
                        user_id = newuser.id,
                        gender=row['Gender'],
                        father_name=row['Father Name'],
                        father_occ=row['Father Occupation'],
                        father_phone=row['Father Phone'],
                        mother_name=row['Mother Name'],
                        mother_tounge=row['Mother Tounge'],
                        dob=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        blood_group=row['Blood Group'],
                        phone=row['Phone'],
                        dno_sn=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city_name=row['City Name'],
                        state_name=row['State Name'],
                        country_name=row['Country'],
                        branch=row['Branch']
                    )
                ])
        return HttpResponse('Bulk Upload Done.')
    else:
        return HttpResponse('Something Went Wrong!')

def bulk_upload_staffs(request):
    return render(request, 'oncl_app/testing2.html')

def bulk_upload_staffs_save(request):
    if request.method == 'POST':
        staff_from_db = User.objects.all()
        staff_user=[]
        for i in staff_from_db:
            staff_user.append(i.username)
            staff_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['studentfile'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in staff_user and str(row['Email']) not in staff_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First_Name'],
                    last_name=row['Last_Name'],
                    email=row['Email'],
                    password=row['Password'],
                )
                Faculty=Group.objects.get(name='Faculty')
                if row['Group'] == 'Faculty':
                    Faculty.user_set.add(newuser)
                    newuser.groups.add(Faculty)

                staff = Staffs.objects.bulk_create([
                    Staffs(
                        user_id = newuser.id,
                        gender=row['Gender'],
                        father_name=row['Father Name'],
                        father_occ=row['Father Occupation'],
                        father_phone=row['Father Phone'],
                        mother_name=row['Mother Name'],
                        mother_tounge=row['Mother Tounge'],
                        dob=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        blood_group=row['Blood Group'],
                        phone=row['Phone'],
                        dno_sn=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city_name=row['City Name'],
                        state_name=row['State Name'],
                        country_name=row['Country'],
                        branch=row['Branch'],
                        designation=row['Desgination'],
                        qualification=row['Qualification']
                    )
                ])
        return HttpResponse('Bulk Upload Done.')
    else:
        return HttpResponse('Something Went Wrong!')