from django import forms
from .models import Employees

class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['emp_name', 'emp_designation', 'emp_qualification', 'emp_salary', 'status', 'employee_email']
        widgets = {
            'emp_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Name'}),
            'emp_designation': forms.Select(attrs={'class': 'form-control'}),
            'emp_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'employee_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'emp_name': 'Employee Name',
            'employee_email': 'Employee Email',
        }
