from django.core.mail import send_mail
import random
from django.utils import timezone
from django.conf import settings
from account.models import Users


def send_otp(email):

    otp=random.randint(1000,9999)
    
    subject = "Account Verification OTP"
    masked_email = mask_email(email)
    message = f"Hello,\n\nYour OTP for account verification is: {otp}\n\nThis OTP is valid for the next 5 minute.\n\nIf you did not request this OTP, please ignore this email\nOr go through this url and enter otp click here >> http://localhost:8000/verify/{masked_email}/.\n\nThank you,\nYour Application Team"

    email_from=settings.EMAIL_HOST

    send_mail(subject, message, email_from, [email])

    user_obj=Users.objects.get(email = email)
    user_obj.otp = otp
    user_obj.otp_expiration = timezone.now() + timezone.timedelta(minutes=5) 
    user_obj.save()

    return user_obj



def mask_email(email):
    """Mask email for display, e.g., ro****0@gmail.com."""
    parts = email.split("@")
    local = parts[0]
    domain = parts[1]
    masked_local = local[0] + "****" + local[-1]
    return masked_local + "@" + domain  


def otp_is_valid(email, otp):
    """Check if the provided OTP is valid for the given email and not expired."""
    try:
        user = Users.objects.get(email=email, otp=otp)
        if user.otp_expiration > timezone.now():
            return True
    except Users.DoesNotExist:
        return False
    return False
