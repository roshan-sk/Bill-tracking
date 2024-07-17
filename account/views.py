from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from helper.forgot_password_email import send_email_for_forgot, decrypt_data
from .models import Bill, Users
from helper.email import send_otp, mask_email, otp_is_valid
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer
from django.http import HttpResponseNotAllowed

from cryptography.fernet import InvalidToken
from django.db.models import Q


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
    request.session['original_email']='roshansk@gmail.com'

    return render(request, "home.html", {'bills': bills})  # Pass the bills to the template


def add_item(request):
    if request.method == 'POST':
        name_of_item = request.POST['name_of_item']
        description = request.POST['description']
        price = request.POST['price']
        
        # Create a new Bill object and save it to the database
        new_bill = Bill(name_of_item=name_of_item, description=description, price=price)
        new_bill.save()
        
        return redirect('home')  # Redirect to the home page after adding the item

    return render(request, 'add_item.html')


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


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif Users.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif Users.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            hashed_password = make_password(password)
            user = Users.objects.create(username=username, email=email, first_name=firstName, last_name=lastName, password=hashed_password)
            send_otp(user.email)
            masked_email = mask_email(user.email)
            request.session['original_email'] = user.email
            messages.success(request, "Verify your email")
            return redirect('verify', masked_email=masked_email)

    return render(request, "registration.html")
    


def verify_otp(request, masked_email):
    if request.method == 'POST':
        otp = request.POST['otp']
        original_email = request.session.get('original_email')

        if otp_is_valid(original_email, otp):
            user = Users.objects.get(email=original_email)
            user.is_verified = True
            user.save()
            messages.success(request, "Email verified successfully")
            return redirect("webpage")
        else:
            messages.error(request, "Invalid OTP or OTP expired")
    return render(request, "verify.html", {'masked_email': masked_email})


def resend_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                # Check if the email exists in the database
                user = Users.objects.get(email=email)
                # Send OTP to the provided email
                send_otp(email)
                request.session['original_email'] = email  # Store email in session for verification
                messages.success(request, f"OTP has been resent to {mask_email(email)}.")
                return redirect('verify', masked_email=mask_email(email))
            except Users.DoesNotExist:
                messages.error(request, "The provided email does not exist in our records.")
                return redirect('register')
        else:
            messages.error(request, "Please provide a valid email.")
            return redirect('register')

    # If request method is not POST, redirect to register page
    return redirect('register')
    


def login_view(request):
    if request.method == 'POST':
        # Handle POST request for authentication
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)  # Find user by email
            # print(user)
        except Users.DoesNotExist:
            messages.error(request, 'Invalid credentials. User does not exist.')
            return redirect('login')  # Redirect back to login page with error message

        # Check if password matches
        if not check_password(password, user.password):
            messages.error(request, 'Invalid credentials. Password incorrect.')
            return redirect('login')  # Redirect back to login page with error message

        # Check if user is verified (adjust as per your user model)
        if not user.is_verified:
            messages.error(request, 'User is not verified.')
            return redirect('login')  # Redirect back to login page with error message

        # Login successful, set user in session (if using session-based authentication)
        # request.session['user_id'] = user.id  # Example of setting user in session

        messages.success(request, 'Login successful.')
        return redirect('bills/')  # Replace 'webpage' with your actual home URL name

    elif request.method == 'GET':
        # Handle GET request to render the login form
        return render(request, 'signIn.html')  # Replace 'signIn.html' with your actual template name

    else:
        # Return method not allowed for any other request method
        return HttpResponseNotAllowed(['POST'])  # Handle other methods as needed
    


def webpage(request):
    products = Users.objects.all()
    context = {
        'products': products
    }
    return render(request, 'webpage.html', context)



def forgot_password(request):
    if request.method == 'POST':
        user_email = request.POST.get('email').strip()  # Correct syntax: use request.POST.get('email')
        print(user_email)

        print(Users.objects.filter(email=user_email).exists())
        if Users.objects.filter(email=user_email).exists():  # Correct model name: User, not Users
            send_email_for_forgot(user_email)
            messages.success(request, "An email has been sent to reset your password.")
        else:
            messages.error(request, "Email is not registered.")
    
    # Render the same template with messages displayed
    return render(request, "forgot_password.html")
    


def reset_password(request, encrypted_email):
    try:
        email = decrypt_data(encrypted_email)
        user = Users.objects.get(email=email)
        return render(request, 'reset_password.html', {'email': email})
    except Users.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('password_reset')  # Redirect to password reset form or home page
    except InvalidToken as e:
        messages.error(request, 'Invalid password reset link.')
        return redirect('password_reset')  # Redirect to password reset form or home page

def reset_password_submit(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password', encrypted_email=request.POST.get('encrypted_email'))

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login')  # Redirect to login page
    else:
        return redirect('login')