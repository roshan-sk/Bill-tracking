# Import necessary modules
from cryptography.fernet import Fernet
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Generate a key (run this once and store the key securely)
key = Fernet.generate_key()
# print(key)

# Save the key to a file (for development purposes)
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Load the key from the file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Initialize Fernet with the loaded key
cipher_suite = Fernet(key)

# Function to encrypt data
def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()

# Function to decrypt data
def decrypt_data(encrypted_data):
    print(encrypted_data)
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
    print(decrypted_data)
    return decrypted_data

# Function to send password reset email
def send_email_for_forgot(email):
    encrypted_email = encrypt_data(email)
    print(email, encrypted_email)
    print(decrypt_data(encrypted_email))
    reset_url = f"http://localhost:8000/reset_password/{encrypted_email}/"
    message = (
        f"Hello,\n\n"
        f"Please click the following link to reset your password:\n"
        f"{reset_url}\n\n"
        f"If you did not request a password reset, please ignore this email.\n\n"
        f"Thank you,\n"
        f"Your Application Team"
    )

    subject = "Password Reset Request"
    email_from = settings.EMAIL_HOST_USER  # Ensure this matches your Django settings

    send_mail(subject, message, email_from, [email])

# send_email_for_forgot('roshansk032@gmail.com')

# Example Django view for handling password reset request
# def forgot_password_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(email=email)
#             send_email_for_forgot(email)
#             messages.success(request, 'An email has been sent with instructions to reset your password.')
#             return redirect('password_reset_done')
#         except User.DoesNotExist:
#             messages.error(request, 'Email does not exist.')
#             return redirect('password_reset')
    
#     return render(request, 'password_reset_form.html')
