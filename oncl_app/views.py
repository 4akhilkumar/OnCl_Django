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
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import template
import json
import datetime

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
from .forms import CreateUserForm, ContactForm, PositionForm, StaffsForm, StudentsForm, MyfileUploadForm, SessionUploadForm
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
def te_page(request):
    return render(request, 'oncl_app/login_register/register_mail.html')

def whin_page(request):
    return render(request, 'oncl_app/static_files_folder/whin.html')

def oncl_page(request):
    return render(request, 'oncl_app/static_files_folder/OnCl.html')

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
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            group = Group.objects.get(name='Faculty')
            user.groups.add(group)

            context = {'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name}
            template = render_to_string('oncl_app/login_register/register_mail.html', context)
            send_mail(first_name + ', welcome to your new OnCl Account', template, settings.EMAIL_HOST_USER, [email], html_message=template)				
            
            messages.success(request, 'Hey ' + username + '! Your Account is Created Succesfully!')
            return redirect('login')
    context = {'form':form}
    return render(request, 'oncl_app/login_register/register.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            template = render_to_string('oncl_app/login_register/login_mail.html', {'email':request.user.email})
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
	return redirect('login')

@unauthenticated_user
def dashboard_page(request):
	username = request.user.get_username()
	return #

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def dashboard_student_page(request):
	username = request.user.get_username()
	return render(request, 'oncl_app/dashboard_student.html', {'username':username})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Faculty'])
def dashboard_faculty_page(request):
	username = request.user.get_username()
	return render(request, 'oncl_app/dashboard_faculty.html', {'username':username})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def dashboard_admin_page(request):
	username = request.user.get_username()
	return render(request, 'oncl_app/dashboard_admin.html', {'username':username})

class PCS_Cloud_List(ListView):
    model = PCS_Cloud
    context_object_name = 'sessions'

class PCS_Cloud_Detail(DetailView):
    model = PCS_Cloud
    context_object_name = 'session'
    template_name = 'oncl_app/PCS_cloud/session.html'

class PCS_Cloud_Create(CreateView):
    model = PCS_Cloud
    fields = '__all__'
    success_url = reverse_lazy('pcs_cloud')

class PCS_Cloud_Update(UpdateView):
    model = PCS_Cloud
    fields = '__all__'
    success_url = reverse_lazy('pcs_cloud')

class PCS_Cloud_Delete(DeleteView):
    model = PCS_Cloud
    context_object_name = 'session'
    success_url = reverse_lazy('pcs_cloud')

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
    return render(request, "oncl_app/admin_templates/semester_templates/add_semester.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_semester_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_branch')
    else:
        semester_start_year = request.POST.get('semester_start_year')
        semester_end_year = request.POST.get('semester_end_year')

        try:
            semesteryear = Semester(semester_start_year=semester_start_year, semester_end_year=semester_end_year)
            semesteryear.save()
            messages.success(request, "Semester Added Successfully.")
            return redirect("manage_semester")
        except:
            messages.error(request, "Failed to Add Semester Year!")
            return redirect("add_semester")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_semester(request, semester_id):
    semester_year = Semester.objects.get(id=semester_id)
    context = {
        "semester_year": semester_year
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
        semester_start_year = request.POST.get('semester_start_year')
        semester_end_year = request.POST.get('semester_end_year')

        try:
            semester_year = Semester.objects.get(id=semester_id)
            semester_year.semester_start_year = semester_start_year
            semester_year.semester_end_year = semester_end_year
            semester_year.save()

            messages.success(request, "Semester Updated Successfully.")
            return redirect('manage_semester')
        except:
            messages.error(request, "Failed to Update Semester!.")
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
    semester_years = Semester.objects.all()
    context = {
        "semester_years": semester_years
    }
    return render(request, "oncl_app/admin_templates/semester_templates/manage_semester.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_branch(request):
    return render(request, "oncl_app/admin_templates/branch_templates/add_branch.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_branch_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_branch')
    else:
        branch = request.POST.get('branch')
        try:
            branch_model = Branches(branch_name=branch)
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
    context = {
        "branch": branch,
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
            branch.branch_name = branch_name
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
    courses = Branches.objects.all()
    staffs = User.objects.filter(groups='2')
    context = {
        "courses": courses,
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

        course_id = request.POST.get('course')
        course = Branches.objects.get(id=course_id)
        
        staff_id = request.POST.get('staff')
        staff = User.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
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
    courses = Branches.objects.all()
    staffs = User.objects.filter(groups='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
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
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Branches.objects.get(id=course_id)
            subject.course_id = course

            staff = User.objects.get(id=staff_id)
            subject.staff_id = staff
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return redirect('manage_subject')
            # return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject!")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            # return redirect('/edit_subject/'+subject_id)

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
        staff_form = StaffsForm(request.POST)

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
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
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
@allowed_users(allowed_roles=['Admin'])
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
        git_link = request.POST.get('git_link')
        website_link = request.POST.get('website_link')
        linkedin_link = request.POST.get('linkedin_link')
        orcid_link = request.POST.get('orcid_link')
        researcher_link = request.POST.get('researcher_link')
        gscholar_link = request.POST.get('gscholar_link')
        microsoft_academic_link = request.POST.get('microsoft_academic_link')
        bio = request.POST.get('bio')
        profile_pic = request.POST.get('profile_pic')

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
            staff_model.bio = bio
            staff_model.branch = branch
            staff_model.desgination = desgination
            staff_model.address = address
            staff_model.qualification = qualification
            staff_model.profile_pic = profile_pic
            staff_model.git_link = git_link
            staff_model.website_link = website_link
            staff_model.linkedin_link = linkedin_link
            staff_model.orcid_link = orcid_link
            staff_model.researcher_link = researcher_link
            staff_model.gscholar_link = gscholar_link
            staff_model.microsoft_academic_link = microsoft_academic_link
            staff_model.save()

            messages.success(request, "Faculty Updated Successfully.")
            # return redirect('/edit_staff/'+staff_id)
            return redirect('manage_staff')

        except:
            messages.error(request, "Failed to Update Faculty!")
            return redirect('/edit_staff/'+staff_id+"/")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_staff(request, staff_id):
    staff = Staffs.objects.get(user=staff_id)
    try:
        staff.delete()
        staff.user.delete()
        messages.success(request, "Faculty Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Faculty!")
        return redirect('manage_staff')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_student(request):
    form = CreateUserForm()
    student_form = StudentsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        student_form = StudentsForm(request.POST)

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
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, "oncl_app/admin_templates/student_templates/manage_student.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def edit_student(request, student_id):
    student = Students.objects.get(user=student_id)

    context = {
        "student": student,
        "id": student_id
    }
    return render(request, "oncl_app/admin_templates/student_templates/edit_student.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def view_student(request, student_id):
    student = Students.objects.get(user=student_id)

    context = {
        "student": student,
        "id": student_id
    }
    return render(request, "oncl_app/profile_templates/admin_student_view_profile.html", context)

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
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        branch = request.POST.get('branch')
        phone = request.POST.get('phone')
        git_link = request.POST.get('git_link')
        website_link = request.POST.get('website_link')
        linkedin_link = request.POST.get('linkedin_link')
        bio = request.POST.get('bio')
        profile_pic = request.POST.get('profile_pic')

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
            student_model.address = address
            student_model.gender = gender
            student_model.branch = branch
            student_model.phone = phone
            student_model.git_link = git_link
            student_model.website_link = website_link
            student_model.linkedin_link = linkedin_link
            student_model.bio = bio
            student_model.profile_pic = profile_pic
            student_model.save()

            messages.success(request, "Student Updated Successfully.")
            return redirect('manage_student')
        
        except:
            messages.error(request, "Failed to Update Student!")
            return redirect('/edit_student/'+student_id+"/")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_student(request, student_id):
    student = Students.objects.get(user=student_id)
    try:
        student.delete()
        student.user.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student!")
        return redirect('manage_student')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'oncl_app/admin_templates/permission_templates/student_permissions.html', context)

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
def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'oncl_app/admin_templates/permission_templates/faculty_permissions.html', context)

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
@allowed_users(allowed_roles=['Admin','Faculty'])
def add_announcement(request):
    return render(request, "oncl_app/admin_templates/announcements_templates/add_announcement.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def add_announcement_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_announcement')
    else:
        announcement = request.POST.get('announcement')
        sub_an = request.POST.get('sub_an')
        try:
            announcement_model = Announcements_news(what_an=announcement,sub_an=sub_an)
            announcement_model.save()
            messages.success(request, "Announcement Added Successfully.")
            return redirect('manage_announcement')
        except:
            messages.error(request, "Failed to Add Announcement!")
            return redirect('add_announcement')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student'])
def manage_announcement(request):
    announcements = Announcements_news.objects.all()
    context = {
        "announcements": announcements
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
        what_an = request.POST.get('announcement')
        sub_an = request.POST.get('sub_an')

        try:
            announcement = Announcements_news.objects.get(id=announcement_id)
            announcement.what_an = what_an
            announcement.sub_an = sub_an
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
        messages.success(request, "Announcement Deleted Successfully.")
        return redirect('manage_announcement')
    except:
        messages.error(request, "Failed to Delete Announcement!")
        return redirect('manage_announcement')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def admin_profile(request):
    username = request.user.get_username()
    context={
            'username':username
        }
    return render(request, 'oncl_app/profile_templates/admin_profile.html', context)

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
    context = {
            'username':username, 'student':student, "user": user
        }
    return render(request, 'oncl_app/profile_templates/student_profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Librarian'])
def upload(request):
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST,request.FILES)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            book_name = form.cleaned_data['book_name']
            book_author = form.cleaned_data['book_author']
            book_desc = form.cleaned_data['book_desc']
            book_pub_date = form.cleaned_data['book_pub_date']
            book_pic = form.cleaned_data['book_pic']
            book_file = form.cleaned_data['book_file']
            book_tag1 = form.cleaned_data['book_tag1']
            book_tag2 = form.cleaned_data['book_tag2']
            book_tag3 = form.cleaned_data['book_tag3']
            book_tag4 = form.cleaned_data['book_tag4']

            file_upload(book_id = book_id,
                        book_name = book_name, 
                        book_author = book_author, 
                        book_desc = book_desc,
                        book_pub_date = book_pub_date,
                        book_pic = book_pic,
                        book_file = book_file,
                        book_tag1 = book_tag1,
                        book_tag2 = book_tag2,
                        book_tag3 = book_tag3,
                        book_tag4 = book_tag4).save()
            return HttpResponse("Book Uploaded Successfully.")
        else:
            return HttpResponse('Failed to Upload Book!')
    else:
        context={
            'form': MyfileUploadForm()
        }
        return render(request, "oncl_app/E-Library/upload_book.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def view_books(request):
    all_data = file_upload.objects.all()
    context = {
        'data':all_data
    }
    return render(request,'oncl_app/E-Library/view_books.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def search(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        query = request.POST['search']
        books = file_upload.objects.filter(
            Q(book_id__contains=query) | Q(book_name__contains=query) | 
            Q(book_author__contains=query) | Q(book_desc__contains=query) | 
            Q(book_pub_date__contains=query) | Q(book_tag1__contains=query) | 
            Q(book_tag2__contains=query) | Q(book_tag3__contains=query) | 
            Q(book_tag4__contains=query))
        now1 = datetime.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/E-Library/search_books.html', {'books': books, 'cal_time':cal_time})
    else:
        all_data = file_upload.objects.all()
        context = {
            'data': all_data 
        }
        return render(request, 'view.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def search_announcements(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        query = request.POST['search']
        announcements = Announcements_news.objects.filter(
            Q(sub_an__contains=query) | Q(what_an__contains=query) | 
            Q(created_at__contains=query) | Q(updated_at__contains=query))
        now1 = datetime.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/admin_templates/announcements_templates/search_announcements.html', {'announcements': announcements, 'cal_time':cal_time})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def search_faculty(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        query = request.POST['search']
        staff = Staffs.objects.filter(Q(gender__contains=query) | Q(address__contains=query))

        now1 = datetime.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/admin_templates/faculty_templates/search_faculty.html', {'staffs': staff, 'cal_time':cal_time})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def search_student(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        query = request.POST['search']
        student = Students.objects.filter(
            Q(branch__contains=query) | Q(address__contains=query) |
            Q(gender__contains=query) | Q(phone__contains=query) |
            Q(linkedin_link__contains=query) | Q(twitter_link__contains=query) |
            Q(git_link__contains=query) | Q(website_link__contains=query))

        now1 = datetime.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/admin_templates/student_templates/search_student.html', {'students': student, 'cal_time':cal_time})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty'])
def upload_session(request):
    if request.method == 'POST':
        form = SessionUploadForm(request.POST,request.FILES)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            session_name = form.cleaned_data['session_name']
            session_author = form.cleaned_data['session_author']
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
                        session_desc = session_desc,
                        session_pub_date = session_pub_date,
                        session_pic = session_pic,
                        session_file = session_file,
                        session_tag1 = session_tag1,
                        session_tag2 = session_tag2,
                        session_tag3 = session_tag3,
                        session_tag4 = session_tag4).save()
            return HttpResponse("Session Uploaded Successfully.")
        else:
            return HttpResponse('Failed to Upload Session!')
    else:
        context={
            'form': SessionUploadForm()
        }
        return render(request, "oncl_app/PCS_Cloud/upload_session.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def view_session(request):
    all_data = PCS_Cloud.objects.all()
    context = {
        'data':all_data
    }
    return render(request,'oncl_app/PCS_Cloud/view_sessions.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Faculty','Student','Librarian'])
def search_session(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        query = request.POST['search']
        sessions = PCS_Cloud.objects.filter(
            Q(session_id__contains=query) | Q(session_name__contains=query) | 
            Q(session_author__contains=query) | Q(session_desc__contains=query) | 
            Q(session_pub_date__contains=query) | Q(session_tag1__contains=query) | 
            Q(session_tag2__contains=query) | Q(session_tag3__contains=query) | 
            Q(session_tag4__contains=query))
        now1 = datetime.datetime.now()
        cal_time = (now1 - now).total_seconds()

        return render(request, 'oncl_app/PCS_Cloud/search_sessions.html', {'sessions': sessions, 'cal_time':cal_time})