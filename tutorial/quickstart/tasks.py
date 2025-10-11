from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
import time

@shared_task
def send_welcome_email(user_id):

    try:
        user = User.objects.get(id=user_id)
        print(f"Task started: Sending welcome email to {user.email}")

        time.sleep(10)

        subject = f"Welcome to our platform, {user.username}!"
        message = f"Hi {user.username},\n\nThank you for registering. We are excited to have you with us."
        from_email = "no-reply@oursite.com"
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        print(f"Task finished: Welcome email sent successfully to {user.email}")
        return f"Email sent to {user.email}"
    except User.DoesNotExist:
        print(f"Task failed: User with id {user_id} does not exist.")
        return f"User with id {user_id} not found."