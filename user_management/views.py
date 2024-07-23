from django.shortcuts import render, get_object_or_404, redirect
from .models import Employees
from .forms import EmployeesForm

# List all employees
def employee_list(request):
    employees = Employees.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

# Create a new employee
def employee_create(request):
    if request.method == "POST":
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeesForm()
    return render(request, 'employee_form.html', {'form': form})

# Update an existing employee
def employee_update(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == "POST":
        form = EmployeesForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeesForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

# Delete an employee
def employee_delete(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})
