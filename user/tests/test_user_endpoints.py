import json
import io

from PIL import Image

from unittest.mock import patch


from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from user.tests.factories import UserFactory
from user.models import UserProfile, User
from user.messages.success import USER_CREATED, LOGIN_SUCCESSFULL, PROFILE_UPDATED, USER_RETRIEVED
from user.messages.error import LOGIN_FAIL, INVALID_PASSPORT, NO_TOKEN
from flighty.messages.error import COULD_NOT_DECODE_TOKEN, DEACTIVATED_USER, DELETED_USER

class TestUserEndpoint(APITestCase):

    def _auth_header(self, token):
        return f'Bearer {token}'

    def _login(self, data):
        url = reverse('user:signin')
        return self.client.post(url, data, format='json')
    
    def _generate_passport(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        password = 'password'
        self.admin = UserFactory(
            is_staff=True,
            email='admin@test.com',
            password=password
        )
        self.user = UserFactory(
            email='user@test.com',
            password=password
        )
        
        admin_token = self._login(dict(email=self.admin.email, password=password)).data['data']['token']
        
        self._admin_header = self._auth_header(admin_token)

        token = self._login(dict(email=self.user.email, password=password)).data['data']['token']

        self._header = self._auth_header(token)
        print('==================User')

    
    def test_user_signup_with_valid_data_succeeds(self):
        url = reverse('user:signup')
        data = {
            'email': 'user1@test.com',
            'password': 'password'
        }

        response = self.client.post(url, 
        data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['message'], USER_CREATED)
        self.assertEqual(response_data['data']['email'], data['email'])
        assert 'token' in response_data['data']
        assert len(UserProfile.objects.filter(user__email=data['email']).all()) == 1

    def test_create_existing_users_fails(self):
        url = reverse('user:signup')
        data = {
            'email': self.admin.email,
            'password': 'password'
        }

        response = self.client.post(url, 
        data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['errors']['email'][0], 'user with this email already exists.')
        assert len(UserProfile.objects.filter(user__email=data['email']).all()) == 1

    def test_user_signup_with_invalid_data_fails(self):
        url = reverse('user:signup')
        data = {
            'email': 'user1@test',
            'password': 'password'
        }

        response = self.client.post(url, 
        data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['errors']['email'][0], 'Enter a valid email address.')

    def test_user_signup_with_incomplete_data_fails(self):
        url = reverse('user:signup')
        data = {
            'email': 'user1@test.com',
        }

        response = self.client.post(url, 
        data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['errors']['password'][0], 'This field is required.')

    def test_user_signin_with_valid_data_succeeds(self):
        data = {
            'email': 'user@test.com',
            'password': 'password'
        }
        
        response = self._login(data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'], LOGIN_SUCCESSFULL)
        self.assertEqual(response_data['data']['email'], data['email'])
        assert 'token' in response_data['data']
        self.token = response_data['data']['token']

    def test_user_signin_not_found_fails(self):
        url = reverse('user:signin')
        data = {
            'email': 'user1@test',
            'password': 'password'
        }

        response = self.client.post(url, 
        data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['errors']['error'][0], LOGIN_FAIL)

    def test_user_signin_with_incomplete_data_fails(self):
        url = reverse('user:signin')
        data = {
            'email': 'user1@test.com',
        }

        response = self.client.post(url, 
        data, format='json')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['errors']['password'][0], 'This field is required.')

    def test_update_profile_with_valid_data_succeeds(self):
        url = reverse('user:profile')
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname'
        }

        response = self.client.patch(url, 
        data, format='json', HTTP_AUTHORIZATION=self._header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'], PROFILE_UPDATED)
        self.assertEqual(response_data['data']['userprofile']['first_name'], data['first_name'])
        assert 'token' in response_data['data']
        self.assertEqual(response_data['data']['userprofile']['last_name'], data['last_name'])

    def test_upload_passport_succeeds(self):
        url = reverse('user:profile')
        data = {
            'image': self._generate_passport()
        }
        
        image_name_list = data['image'].name.split('.')
        response = self.client.patch(url, 
        data, format='multipart', HTTP_AUTHORIZATION=self._header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'], PROFILE_UPDATED)

        assert response_data['data']['userprofile']['image'].startswith('/media/' + image_name_list[0])

        assert response_data['data']['userprofile']['image'].endswith(image_name_list[-1])

    def test_upload_invalid_passport_fails(self):
        url = reverse('user:profile')
        data = {
            'image': ''
        }
        
        response = self.client.patch(url, 
        data, format='multipart', HTTP_AUTHORIZATION=self._header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['errors']['userprofile']['image'][0], INVALID_PASSPORT)

    # @patch('user.tasks.delete_passport_image')
    # @patch('user.tasks.os.remove')
    # def test_delete_passport_succeeds(self, remove, delete_passport_image):
    #     url = reverse('user:profile') + '?deleteImage=true'
    #     data = {
    #         'image': self._generate_passport()
    #     }
        
    #     response = self.client.patch(url, 
    #     data, format='multipart', HTTP_AUTHORIZATION=self._header)
    #     response_data = response.data
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_data['data']['userprofile']['image'], None)
    #     print('dir', dir(delete_passport_image))
    #     assert delete_passport_image.assert_called_once
    #     assert remove.assert_called_once

    def test_get_user_with_valid_token_succeeds(self):
        url = reverse('user:profile')
        
        response = self.client.get(url, HTTP_AUTHORIZATION=self._header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['userprofile']['image'], '/media/' + self.user.userprofile.image.name)
        self.assertEqual(response_data['data']['email'], self.user.email)

    def test_get_user_with_no_token_fails(self):
        url = reverse('user:profile')
        
        response = self.client.get(url, HTTP_AUTHORIZATION='')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], NO_TOKEN)

    def test_get_user_with_invalid_token_fails(self):
        url = reverse('user:profile')
        
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer EJEHE')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], COULD_NOT_DECODE_TOKEN)

    def test_decode_token_for_len_one_fails(self):
        url = reverse('user:profile')
        
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], NO_TOKEN)

    def test_decode_token_for_len_gt_two_fails(self):
        url = reverse('user:profile')
        
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer 1 1')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], NO_TOKEN)

    def test_decode_with_invalid_prefix_fails(self):
        url = reverse('user:profile')
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearerrrr')
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], NO_TOKEN)
    
    def test_token_with_deactivated_fails(self):
        url = reverse('user:profile')
        user = User.objects.filter(email=self.user.email).first()
        user.is_active = False
        user.save()
        response = self.client.get(url, HTTP_AUTHORIZATION=self._header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], DEACTIVATED_USER)

    def test_token_with_deleted_user_fails(self):
        url = reverse('user:profile')
        User.objects.filter(email=self.user.email).delete()
        response = self.client.get(url, HTTP_AUTHORIZATION=self._header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data['detail'], DELETED_USER)