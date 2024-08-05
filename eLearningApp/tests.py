# tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Institution, User, AppUser

class UserAPITests(APITestCase):
    
    def setUp(self):
        self.institution = Institution.objects.create(name='The Test Uni', location="The World")  # Create the institution
        # Create a user and store the user ID
        self.user = User.objects.create_user(
            email='apitest@test.com',
            password='testpassword',
            username='apitest@test.com',
            first_name='Test',
            last_name='User',
        )
        self.appuser = AppUser.objects.create(user=self.user, institution=self.institution)  # Create the app user
        self.user_id = self.user.id
        
        
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        data = {
            'email': 'apitest2@test.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'institution': 'The Test Uni'
        }

        response = self.client.post(reverse('api_user', kwargs={'pk': self.user_id}), data, format='json')
        self.user_id = User.objects.get(username=response.data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_users(self):
        """
        Ensure we can get a specific user object.
        """
        response = self.client.get(reverse('api_user', kwargs={'pk': self.user_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'apitest@test.com')
        
    def test_get_all_users(self):
        """
        Ensure we can get all user objects.
        """
        response = self.client.get(reverse('api_users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_delete_user(self):
        """
        Ensure we can delete a specific user object.
        """
        response = self.client.delete(reverse('api_user', kwargs={'pk': self.user_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)