from rest_framework.test import APITestCase
from user.models import User

class TestUserModel(APITestCase):

    def setUp(self):
        password = 'password'
        self.password = password
    
    def test_create_super_user(self):
        user = User.objects.create_superuser('admin@test.com', self.password)
        self.assertEqual(user.email, 'admin@test.com')
        user.userprofile.get_full_name()
        repr(user.userprofile)
        repr(user)

    def test_create_super_user_with_no_email_fails(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(None, self.password)
        
    def test_create_super_user_with_no_password_fails(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser('admin@test.com', None)