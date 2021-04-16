from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import TaskList, TaskCreate, TaskUpdate, DeleteView, TaskReorder
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('login/', views.login_page, name = 'login'),
    path('register/', views.register_page, name = 'register'),
	path('logout/', views.logoutUser, name="logout"),
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="oncl_app/password_reset/password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="oncl_app/password_reset/password_reset_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="oncl_app/password_reset/password_reset_form.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="oncl_app/password_reset/password_reset_complete.html"),
        name="password_reset_complete"),
    
    path('feedback/', views.feedback_page, name='feedback'),
    path('success/', views.successView, name='success'),

    path('audio/', views.audio_page, name = 'audio'), 

    path('tasks/', 
        TaskList.as_view(template_name="oncl_app/task/task_list.html"),
        name='tasks'),
    path('task-create/',
        TaskCreate.as_view(template_name="oncl_app/task/task_form.html"),
        name='task-create'),
    path('task-update/<int:pk>/',
        TaskUpdate.as_view(template_name="oncl_app/task/task_form.html"),
        name='task-update'),
    path('task-delete/<int:pk>/',
        DeleteView.as_view(template_name="oncl_app/task/task_confirm_delete.html"),
        name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    path('dashboard/', views.dashboard_page, name = 'dashboard'),

    re_path(r'^.*\.*', views.pages, name='pages'),
]