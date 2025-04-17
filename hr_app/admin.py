from django.contrib import admin
from .models import Employee, Payroll, Attendance, Review, LeaveRequest

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'salary', 'total_salary')
    search_fields = ('employee__first_name', 'employee__last_name', 'month', 'year')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'date')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_date', 'rating', 'feedback')
    search_fields = ('employee__first_name', 'employee__last_name', 'review_date')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email')

# Register models with the admin site
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(LeaveRequest)
