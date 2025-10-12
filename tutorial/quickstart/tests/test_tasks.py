from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.test import override_settings
from django.contrib.auth.models import User


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class UserCreationTaskTest(TestCase):
    
    def test_create_user_sends_welcome_email(self):
    

        url = reverse('UsersApi-list') 
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        # locmem.EmailBackend 
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(User.objects.count(), 0)

        
        response = self.client.post(url, user_data, format='json')


        self.assertEqual(response.status_code, 201)

        self.assertEqual(User.objects.count(), 1)

        created_user = User.objects.first()
        self.assertEqual(created_user.username, "testuser")
        self.assertEqual(created_user.email, "test@example.com")

   
        self.assertEqual(len(mail.outbox), 1)
        
        sent_email = mail.outbox[0]
        
        self.assertEqual(sent_email.subject, f"Welcome to our platform, {created_user.username}!")
        self.assertIn("Thank you for registering", sent_email.body)
        self.assertEqual(sent_email.to, ["test@example.com"])
        self.assertEqual(sent_email.from_email, "no-reply@oursite.com")