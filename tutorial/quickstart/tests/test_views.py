from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserViewSetTests(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        self.list_url = reverse("user-list")
        self.detail_url_user2 = reverse("user-detail", kwargs={"pk": self.user2.pk})

    def test_unauthenticated_user_is_denied(self):

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_users(self):

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_create_user_uses_create_serializer(self):

        self.client.force_authenticate(user=self.user1)

        new_user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpassword",
        }

        response = self.client.post(self.list_url, new_user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.data["username"], "newuser")
        self.assertNotIn("password", response.data)

    def test_user_cannot_update_another_user(self):

        self.client.force_authenticate(user=self.user1)

        update_data = {"email": "changed@example.com"}

        response = self.client.put(self.detail_url_user2, update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_own_profile(self):

        self.client.force_authenticate(user=self.user2)

        update_data = {"email": "newemail@example.com"}

        response = self.client.patch(self.detail_url_user2, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "newemail@example.com")

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.email, "newemail@example.com")

class GroupViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.group = Group.objects.create(name="Group1")

        self.list_url = reverse("group-list")
        self.detail_url = reverse("group-detail", kwargs={"pk": self.group.pk})

    def test_unauthenticated_user_cannot_access_groups(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_groups(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        group_names = [group['name'] for group in response.data['results']]
        
        self.assertIn(self.group.name, group_names)

    def test_authenticated_user_can_create_group(self):
        self.client.force_authenticate(user=self.user)
        new_group_data = {"name": "NewGroup"}
        response = self.client.post(self.list_url, new_group_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 2)
        self.assertEqual(response.data["name"], "NewGroup")

    def test_authenticated_user_can_update_group(self):
        self.client.force_authenticate(user=self.user)
        updated_data = {"name": "Senior Developers"}
        response = self.client.put(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, "Senior Developers")

    def test_authenticated_user_can_delete_group(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 0)
