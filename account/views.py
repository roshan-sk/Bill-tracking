from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Bill

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    
    return render(request, "register.html")



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully", extra_tags='success')
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials", extra_tags='error')
    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect("login")



def home(request):
    bills = Bill.objects.all()  # Query all bills from the Bill model
    return render(request, "home.html", {'bills': bills})  # Pass the bills to the template

def edit_items(request):
    bills = Bill.objects.all()  # Query all bills from the Bill model
    return render(request, "edit_items.html", {'bills': bills})  # Pass the bills to the template

def edit_item(request, item_id):
    bill = get_object_or_404(Bill, id=item_id)
    if request.method == 'POST':
        bill.name_of_item = request.POST['name_of_item']
        bill.description = request.POST['description']
        bill.price = request.POST['price']
        bill.save()
        return redirect('edit_items')

    return render(request, "edit_item.html", {'bill': bill})

def delete_item(request, item_id):
    bill = get_object_or_404(Bill, id=item_id)
    if request.method == 'POST':
        bill.delete()
        return redirect('edit_items')

    return render(request, "delete_item.html", {'bill': bill})