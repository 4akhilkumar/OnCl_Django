from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template

from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core import mail

# Imports for Reordering Feature
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse

from django.db import transaction

from .models import *
from .forms import CreateUserForm, ContactForm, PositionForm
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

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

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
    staffs = User.objects.filter(is_staff=True)
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
    staffs = User.objects.filter(is_staff=True)
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