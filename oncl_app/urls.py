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

    path('add_semester/', views.add_semester, name="add_semester"),
    path('add_semester_save/', views.add_semester_save, name="add_semester_save"),
    path('edit_semester/<semester_id>', views.edit_semester, name="edit_semester"),
    path('edit_semester_save/', views.edit_semester_save, name="edit_semester_save"),
    path('delete_semester/<semester_id>/', views.delete_semester, name="delete_semester"),
    path('manage_semester/', views.manage_semester, name="manage_semester"),

    path('add_branch/', views.add_branch, name="add_branch"),
    path('add_branch_save/', views.add_branch_save, name="add_branch_save"),
    path('manage_branch/', views.manage_branch, name="manage_branch"),
    path('edit_branch/<branch_id>/', views.edit_branch, name="edit_branch"),
    path('edit_branch_save/', views.edit_branch_save, name="edit_branch_save"),
    path('delete_branch/<branch_id>/', views.delete_branch, name="delete_branch"),

    path('add_subject/', views.add_subject, name="add_subject"),
    path('add_subject_save/', views.add_subject_save, name="add_subject_save"),
    path('manage_subject/', views.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', views.edit_subject, name="edit_subject"),
    path('edit_subject_save/', views.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', views.delete_subject, name="delete_subject"),

    path('add_staff/', views.add_staff, name="add_staff"),
    path('manage_staff/', views.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', views.edit_staff, name="edit_staff"),
    path('edit_staff_save/', views.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', views.delete_staff, name="delete_staff"),

    path('add_student/', views.add_student, name="add_student"),
    path('edit_student/<student_id>/', views.edit_student, name="edit_student"),
    path('edit_student_save/', views.edit_student_save, name="edit_student_save"),
    path('manage_student/', views.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', views.delete_student, name="delete_student"),

    path('admin_view_attendance/', views.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', views.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', views.admin_get_attendance_student, name="admin_get_attendance_student"),

    path('student_leave_view/', views.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', views.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', views.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', views.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', views.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', views.staff_leave_reject, name="staff_leave_reject"),

    path('add_announcement/', views.add_announcement, name="add_announcement"),
    path('add_announcement_save/', views.add_announcement_save, name="add_announcement_save"),
    path('manage_announcement/', views.manage_announcement, name="manage_announcement"),
    path('edit_announcement/<announcement_id>/', views.edit_announcement, name="edit_announcement"),
    path('edit_announcement_save/', views.edit_announcement_save, name="edit_announcement_save"),
    path('delete_announcement/<announcement_id>/', views.delete_announcement, name="delete_announcement"),
    
    path('unauthorized_access/', views.unauthorized_access, name='unauthorized_access'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]