'''
Tijana Gasic 0247/2021
'''


from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class LoginTest(TestCase):

    """
    class for testing login functionality
    """

    def setUp(self):

        '''
        sets the initial data
        :return:
        '''

        self.client = Client()

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username='testuser1', password='12345', email='testuser1@example.com')


    def tearDown(self):

        self.client.logout()

    def test_login(self):

        '''
        tests the basic login of a user
        :return:
        '''

        self.client.post(reverse('login-page'), {'username': 'testuser1', 'password': '12345'})

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

    def test_login_wrong_username(self):
        """
        testing to see what happens when incorrect username is inputed
        :return:
        """

        self.client.post(reverse('login-page'), {'username': 'testuser', 'password': '12345'})

        response = self.client.get(reverse('home'))

        self.assertNotEqual(response.status_code, 200)


    def test_login_wrong_password(self):
        """
        testing to see what happens when incorrect password is inputed
        :return:
        """

        self.client.post(reverse('login-page'), {'username': 'testuser1', 'password': 'pogrsnalozinka'})

        response = self.client.get(reverse('home'))

        self.assertNotEqual(response.status_code, 200)


    def test_login_no_data(self):
        """
        testing to see what happens when no data is inputed
        :return:
        """

        self.client.post(reverse('login-page'))

        response = self.client.get(reverse('home'))

        self.assertNotEqual(response.status_code, 200)


    def test_login_too_long_data(self):
        """
        testing to see what happens when the data in datafields are too long
        :return:
        """

        self.client.post(reverse('login-page'), {'username': 'testuser1', 'password': 'r' * 100000})

        response = self.client.get(reverse('home'))

        self.assertNotEqual(response.status_code, 200)




