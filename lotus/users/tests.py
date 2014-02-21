from django.test import TestCase, Client
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.TEST_EMAIL = 'xe313c@gmail.com'
        self.TEST_PASSWORD = 'test_password'
        self.TEST_USERNAME = 'jeong'
        self.TEST_URL = ''
        self.signup()

    def signup(self):
        data = dict(email=self.TEST_EMAIL,
                    user_name=self.TEST_USERNAME,
                    password=self.TEST_PASSWORD)

        client = Client()
        response = client.post('/users/signup', data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 1)

    def test_signup(self):
        data = dict(email='jeong@haegeon.me',
                    password='hello?',
                    user_name='jeong2')

        client = Client()
        response = client.post('/users/signup', data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(User.objects.all()[1].user_name, 'jeong2')

    def test_signup_with_duplicate_email(self):
        data = dict(email=self.TEST_EMAIL,
                    user_name='user test',
                    password='saofhi')

        client = Client()
        response = client.post('/users/signup', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

    def test_signup_with_blank_user_name(self):
        data = dict(email='jeong@haegeon.me',
                    user_name='   ',
                    password='saofhi')

        client = Client()
        response = client.post('/users/signup', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

    def test_signup_with_blank_password(self):
        data = dict(email='jeong@haegeon.me',
                    user_name='jeong2',
                    password='  ')

        client = Client()
        response = client.post('/users/signup', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)        
    
    def test_login(self):
        data = dict(email=self.TEST_EMAIL,
                    password=self.TEST_PASSWORD)

        client = Client()
        client.post('/users/login', data)
        response = client.get('/')
        user = response.context.pop().pop()['user']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.user_name, self.TEST_USERNAME)
        self.assertEqual(user.email, self.TEST_EMAIL)

    def test_login_with_invalid_email(self):
        data = dict(email="jeong@haegeon.me",
                    password=self.TEST_PASSWORD)

        client = Client()
        client.post('/users/login', data)
        response = client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context, None)

    def test_login_with_invalid_password(self):
        data = dict(email=self.TEST_EMAIL,
                    password="hahahahah")

        client = Client()
        client.post('/users/login', data)
        response = client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context, None)

