from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  
    path('add-employee/', views.add_employee, name='add_employee'),
    path('logout/',views.logout_view,name='logout'),
    path('edit_employee/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:pk>',views.delete_employee,name='delete'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/update/', views.update_employee, name='update_employee'),
    path('employee/apply-leave/', views.apply_leave, name='apply_leave'),
    path('process_payroll/', views.process_payroll, name='process_payroll'),
    path('track_attendance/', views.track_attendance, name='track_attendance'),
    path('manage_reviews/', views.manage_reviews, name='manage_reviews'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('leave-applications/', views.view_leave_applications, name='view_leave_applications'),
    path('all-leave-applications/', views.view_all_leaves, name='view_all_leaves'),
    path('approve-leave/<int:pk>/', views.approve_leave, name='approve_leave'),
    path('reject-leave/<int:pk>/', views.reject_leave, name='reject_leave'),

]