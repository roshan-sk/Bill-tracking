from django.db import models

class Employees(models.Model):
    DESIGNATION_CHOICES = [
        ('JD', 'Junior Developer'),
        ('SD', 'Senior Developer'),
        ('FSD', 'Full Stack Developer'),
        ('BD', 'Backend Developer'),
        ('FD', 'Frontend Developer'),
        ('HR', 'HR'),
        ('UIUX', 'UI/UX Developer'),
        ('ACC', 'Accounting'),
    ]

    STATUS_CHOICES = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]

    emp_name = models.CharField(max_length=100)
    emp_designation = models.CharField(max_length=4, choices=DESIGNATION_CHOICES)
    emp_qualification = models.CharField(max_length=50)
    emp_salary = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    employee_email = models.EmailField()

    def __str__(self):
        return self.emp_name
