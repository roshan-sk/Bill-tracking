# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bill
from .forms import BillForm

def bill_list_view(request):
    bills = Bill.objects.all()
    
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
