'''
Tijana Gasic 0247/2021
'''

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class ChangeDataTest(TestCase):

    """
    Test for testing changing data in the app
    """

    def setUp(self):

        '''
        this function is called to set initial state
        :return:
        '''

        self.client = Client()

        self.nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username='testuser1', email='testuser1@example.com', password='12345')
        self.user2 = self.User.objects.create_user(username='testuser2', email='testuser2@example.com', password='12345')

    def _authenticate_user(self):
        login_successful = self.client.login(username='testuser1', password='12345')
        self.assertTrue(login_successful)

    def _send_change_data_request(self, username, password, confirm_password, type):

        """
        sends request to change user data
        :param username:
        :param password:
        :param confirm_password:
        :param type:
        :return: post request
        """

        data = {
            "username": username,
            "password": password,
            "confirm-password": confirm_password,
        }

        if type:
            data['nutricionist'] = 'Nutricionist'

        return self.client.post(reverse('change-data'), data)

    def test_change_data(self):
        """
        test for empty data during the changing data. The state of the
        database for those blank fields should not be changed.
        :return:
        """

        self._authenticate_user()

        response = self._send_change_data_request("testuser4", "", "", 0)

        self.assertEqual(self.User.objects.get(id=self.user1.id).username, "testuser4")

    def test_change_password(self):

        """
        test for changing password during the changing data. The state of the database
        should not be changed if the password is equal to the confirmation password.
        :return:
        """

        self._authenticate_user()

        response = self._send_change_data_request("", "123", "123", 0)

        self.client.logout()

        self.assertFalse(self.client.login(username='testuser1', password='12345'))
        self.assertTrue(self.client.login(username='testuser1', password='123'))

    def test_change_password_confirm(self):

        """
        test for changing password during the changing data. The state of the database
        should not be changed if the password is not equal to the confirmation password.
        if the conformation password is different than password the password stays the same as previous
        :return:
        """

        self._authenticate_user()

        response = self._send_change_data_request("", "123", "1234", 0)

        self.client.logout()

        self.assertFalse(self.client.login(username='testuser1', password='123'))
        self.assertTrue(self.client.login(username='testuser1', password='12345'))



