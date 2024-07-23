# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bill
from .forms import BillForm

from django.utils import timezone
from .forms import SelectMonthYearForm
from django.core.paginator import Paginator

def bill_list_view(request):
    # Order bills by a specific field, e.g., 'created_at'
    bills = Bill.objects.all().order_by('-created_at')

    # Check if there are any bills fetched
    if bills.exists():
        first_bill = bills.first()  # Get the first bill object
        # Print individual attribute values
        print(f"Name of Item: {first_bill.name_of_item}")
        print(f"Description: {first_bill.description}")
        print(f"Price: {first_bill.price}")
        print(f"Created At: {first_bill.created_at}")
    
    return render(request, 'bill_list.html', {'bills': bills})

def bill_create_view(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillForm()
    return render(request, 'bill_create.html', {'form': form})

def bill_update_view(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        bill.name_of_item = request.POST.get('name_of_item', bill.name_of_item)
        bill.description = request.POST.get('description', bill.description)
        bill.price = request.POST.get('price', bill.price)
        bill.save()
        return redirect('bill_list')

    return render(request, 'bill_update.html', {'bill': bill})

def bill_delete_view(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'bill_delete.html', {'bill': bill})


def calculate_bill(request):
    now = timezone.now()
    form = SelectMonthYearForm()
    total_price = None
    no_bills_message = None
    future_month_error = None

    if request.method == 'POST':
        form = SelectMonthYearForm(request.POST)
        if form.is_valid():
            selected_year = int(form.cleaned_data['year'])
            selected_month = int(form.cleaned_data['month'])
            selected_month_name = timezone.datetime(selected_year, selected_month, 1).strftime('%B %Y')

            # Check if the selected month and year are in the future
            if (selected_year > now.year) or (selected_year == now.year and selected_month > now.month):
                future_month_error = "Please select a present or past month."
            else:
                bills = Bill.objects.filter(created_at__year=selected_year, created_at__month=selected_month)
                if bills.exists():
                    total_price = f'of {selected_month_name} - {sum(bill.price for bill in bills)}'
                else:
                    no_bills_message = f"No bills were added in {selected_month_name}."

    return render(request, 'calculate_bill.html', {
        'form': form,
        'total_price': total_price,
        'no_bills_message': no_bills_message,
        'future_month_error': future_month_error
    })

