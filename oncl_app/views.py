from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
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
from django.urls import reverse_lazy

from django.db import transaction

from .models import Task, PCS_Cloud
from .models import *
from .forms import CreateUserForm, ContactForm, PositionForm

# Create your views here.
def te_page(request):
    return render(request, 'oncl_app/login_register/register_mail.html')

def whin_page(request):
    return render(request, 'oncl_app/static_files_folder/whin.html')

def oncl_page(request):
    return render(request, 'oncl_app/static_files_folder/oncl.html')

def home_page(request):
    return render(request,'oncl_app/home.html')

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

def register_page(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data['username']
				email = form.cleaned_data['email']
				first_name = form.cleaned_data['first_name']
				last_name = form.cleaned_data['last_name']
				context = {'username':user, 'email':email, 'first_name':first_name, 'last_name':last_name}
				template = render_to_string('oncl_app/login_register/register_mail.html', context)
				send_mail(first_name + ', welcome to your new OnCl Account', template, settings.EMAIL_HOST_USER, [email], html_message=template)				
				
				messages.success(request, 'Hey ' + user + '! Your Account is Created Succesfully!')
				return redirect('login')
		context = {'form':form}
		return render(request, 'oncl_app/login_register/register.html', context)

def login_page(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				template = render_to_string('oncl_app/login_register/login_mail.html', {'email':request.user.email})
				send_mail('OnCl Account Login Alert', template, settings.EMAIL_HOST_USER, [request.user.email], html_message=template)
				return redirect('dashboard')
			else:
				messages.warning(request, 'Username or Password is Incorrect!')

		context = {}
		return render(request, 'oncl_app/login_register/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def dashboard_page(request):
	username = request.user.get_username()
	return render(request, 'oncl_app/dashboard.html', {'username':username})

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