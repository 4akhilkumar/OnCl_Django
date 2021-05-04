from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import TaskList, TaskCreate, TaskUpdate, DeleteView, TaskReorder, PCS_Cloud_List, PCS_Cloud_Detail, PCS_Cloud_Create, PCS_Cloud_Update, PCS_Cloud_Delete
from . import views

urlpatterns = [
    path('te_page/', views.te_page, name = 'te_page'),

    path('whin_page/', views.whin_page, name = 'whin_page'),
    path('oncl_page/', views.oncl_page, name = 'oncl_page'),

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

    path('dashboard/', views.dashboard_page, name = 'dashboard'),
    path('student_dashboard/', views.dashboard_student_page, name = 'student_dashboard'),
    path('faculty_dashboard/', views.dashboard_faculty_page, name = 'faculty_dashboard'),
    path('admin_dashboard/', views.dashboard_admin_page, name = 'admin_dashboard'),

    path('pcs_cloud/', PCS_Cloud_List.as_view(template_name="oncl_app/PCS_Cloud/PCS_Cloud_List.html"), name='pcs_cloud'),
    path('session/<int:pk>/', PCS_Cloud_Detail.as_view(template_name="oncl_app/PCS_Cloud/session.html"), name='session'),
    path('pcs_cloud_create/', PCS_Cloud_Create.as_view(template_name="oncl_app/PCS_Cloud/PCS_Cloud_Form.html"), name='pcs_cloud_create'),
    path('pcs_cloud_update/<int:pk>/', PCS_Cloud_Update.as_view(template_name="oncl_app/PCS_Cloud/PCS_Cloud_Form.html"), name='pcs_cloud_update'),
    path('pcs_cloud_delete/<int:pk>/', PCS_Cloud_Delete.as_view(template_name="oncl_app/PCS_Cloud/PCS_Cloud_Delete.html"), name='pcs_cloud_delete'),

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

    path('audio/', views.audio_page, name = 'audio'), 

    path('terms_of_service_page/', views.terms_of_service_page, name='terms_of_service_page'),
    path('privacy_policy_page/', views.privacy_policy_page, name='privacy_policy_page'),
    path('cookies_policy_page/', views.cookies_policy_page, name='cookies_policy_page'),
    path('GDPR_privacy_policy_page/', views.GDPR_privacy_policy_page, name='GDPR_privacy_policy_page'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('success/', views.successView, name='success'),
    
    path('unauthorized_access/', views.unauthorized_access, name='unauthorized_access'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]