from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal



class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,null=True)  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_hired = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.department})"



class LeaveApplication(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} leave from {self.start_date} to {self.end_date}"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')])

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.salary = Decimal(self.salary) if not isinstance(self.salary, Decimal) else self.salary
        self.bonus = Decimal(self.bonus) if self.bonus and not isinstance(self.bonus, Decimal) else self.bonus

        self.total_salary = self.salary + (self.bonus or Decimal('0.00'))
        super().save(*args, **kwargs) 

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} - {self.month} {self.year}'



class Review(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    review_date = models.DateField(auto_now_add=True)
    feedback = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.username} leave from {self.start_date} to {self.end_date}"
