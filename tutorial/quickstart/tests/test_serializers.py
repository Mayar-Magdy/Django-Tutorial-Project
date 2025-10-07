from django.test import TestCase
from django.contrib.auth.models import User
from tutorial.quickstart.serializers import UserCreateSerializer, UserSerializer
from django.test import RequestFactory

class UserCreateSerializerTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "test_serializer_user",
            "email": "serializer@test.com",
            "password": "a_very_strong_password"
        }
        self.invalid_data = {
            "email": "invalid@test.com",
            "password": "password"
        }

    def test_valid_data_is_valid(self):
    
        serializer = UserCreateSerializer(data=self.valid_data)
        
        self.assertTrue(serializer.is_valid())

        self.assertEqual(serializer.errors, {})

    def test_invalid_data_is_invalid(self):

        serializer = UserCreateSerializer(data=self.invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_create_method_hashes_password(self):

        serializer = UserCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()

        self.assertIsInstance(user, User)

        self.assertNotEqual(user.password, self.valid_data['password'])

        self.assertTrue(user.check_password(self.valid_data['password']))

class UserSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.factory = RequestFactory()
    
    def test_serialization_contains_expected_fields(self):
    
        request = self.factory.get('/users/') 
        
        serializer = UserSerializer(instance=self.user, context={'request': request})
        
        expected_keys = {'id', 'url', 'username', 'email', 'groups'}
        
        self.assertEqual(set(serializer.data.keys()), expected_keys)
        self.assertNotIn('password', serializer.data)