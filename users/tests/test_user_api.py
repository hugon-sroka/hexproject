"""
Test for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """create and return new user"""
    return get_user_model().create_user(**params)

class PublicUserApiTests(TestCase):
    """test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """test creating if user is successful"""

        payload = {
            'email': 'test@example.com',
            'full_name': 'testname',
            'password': 'test123',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error return if user with certain email already exist"""
        payload = {
            'email': 'test@example.com',
            'full_name': 'testname',
            'password': 'test123',

        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        """test if the password for user is less than a number of minimum chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'full_name': 'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def create_token_for_user(self):
        """test generates token for valid credentials"""
        user_details = {
            'full_name':'testname',
            'email':'test@xmple.com',
            'password':'password123',
        }
        create_user(**user_details)
        payload = {
            'email':user_details['email'],
            'password':user_details['password'],
        }

        res = self.client.post('token', payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_token_bad_credentials(self):
        """test answer for invalid entry data"""
        create_user(email='ssss@exmple.com', password='valid')

        payload = {'email':'password': 'invalid'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password return an error"""

