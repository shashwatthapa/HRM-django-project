from django.shortcuts import render,get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee,Payroll,Attendance,Review,LeaveRequest
from .forms import EmployeeForm,LeaveRequestForm,EmployeeUpdateForm
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from decimal import Decimal



def index(request):
    return render(request,'index.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  
            login(request, user)
            return redirect('admin_dashboard')  
        else:
            messages.error(request, 'Invalid username or password, or you are not authorized.')
    
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')  
    
    employees = Employee.objects.all() 
    return render(request, 'admin_dashboard.html', {'employees': employees})
@login_required
def add_employee(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('admin_dashboard')
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})
@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit.html', {'form': form, 'employee': employee})
@login_required
def delete_employee(request,pk):
    employee = get_object_or_404(Employee,pk=pk)
    employee.delete()
    return redirect('admin_dashboard')

def logout_view(request):
    logout(request)
    return redirect('index')

def employee_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('employee_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'employee_login.html')

@login_required
def employee_dashboard(request):
    employee = Employee.objects.get(user=request.user)

    attendances = Attendance.objects.filter(employee=employee)
    payrolls = Payroll.objects.filter(employee=employee)
    reviews = Review.objects.filter(employee=employee)

    return render(request, 'employee_dashboard.html', {
    'employee': employee,
    'attendances': attendances,
    'payrolls': payrolls,
    'reviews': reviews,
})

@login_required
def update_employee(request):
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = EmployeeUpdateForm(instance=request.user)
    return render(request, 'update_employee.html', {'form': form})
@login_required
def track_attendance(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee')
        date = request.POST.get('attendance_date')
        status = request.POST.get('status')
        employee = Employee.objects.get(id=employee_id)
        Attendance.objects.create(employee=employee, date=date, status=status)
        return redirect('track_attendance')

    employees = Employee.objects.all()
    return render(request, 'track_attendance.html', {'employees': employees})
@login_required
def process_payroll(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        month = request.POST.get('month')
        year = request.POST.get('year')
        
        try:
            salary = Decimal(request.POST.get('salary', '0'))  
        except (ValueError, TypeError):
            salary = Decimal('0')  
        
        bonus = request.POST.get('bonus', '0') 
        try:
            bonus = Decimal(bonus)
        except (ValueError, TypeError):
            bonus = Decimal('0')  
        
        try:
            employee = Employee.objects.get(id=employee_id)
            payroll = Payroll.objects.create(
                employee=employee,
                month=month,
                year=year,
                salary=salary,
                bonus=bonus
            )
        except Employee.DoesNotExist:
            pass

    return render(request, 'process_payroll.html', {'employees': employees})

@login_required
def manage_reviews(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee')
        feedback = request.POST.get('feedback')   
        rating = request.POST.get('rating')    

        try:
            employee = Employee.objects.get(id=employee_id)
            review = Review.objects.create(
                employee=employee,
                feedback=feedback,
                rating=rating
            )
            return redirect('manage_reviews')
        except Employee.DoesNotExist:
            pass

    employees = Employee.objects.all()

    return render(request, 'manage_reviews.html', {'employees': employees})

@login_required
def generate_report(request):
    employees = Employee.objects.all()

    report_data = []
    for employee in employees:
        attendances = Attendance.objects.filter(employee=employee)

        reviews = Review.objects.filter(employee=employee)

        payrolls = Payroll.objects.filter(employee=employee)

        report_data.append({
            'employee': employee,
            'attendances': attendances,
            'reviews': reviews,
            'payrolls': payrolls
        })

    return render(request, 'generate_report.html', {'report_data': report_data})


@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            return redirect('employee_dashboard') 
    else:
        form = LeaveRequestForm()
    return render(request, 'apply_leave.html', {'form': form})

@login_required
def view_leave_applications(request):
    leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-submitted_at')
    return render(request, 'view_leave_application.html', {'leaves': leaves})

@login_required
def view_all_leaves(request):
    leave_applications = LeaveRequest.objects.all().order_by('-id')
    return render(request, 'view_all_leaves.html', {'leave_applications': leave_applications})

@login_required
def approve_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'Approved'
    leave.save()
    return redirect('view_all_leaves')
@login_required
def reject_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'Rejected'
    leave.save()
    return redirect('view_all_leaves')
