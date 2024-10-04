'''
Tijana Gasic 0247/2021
'''


import re

from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegistrationTest(TestCase):
    '''
    class is testing basic registration functionality
    '''

    def setUp(self):
        """
        sets the initial data
        :return:
        """

        self.client = Client()


        self.nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username='testuser1', email='testuser1@example.com', password='12345')

    def _send_register_request(self, username, email, password, confirmpassword, gender, usertype):

        """
        testing basic registration functionality with inputed data. it sends post request with
        that data
        :param username:
        :param email:
        :param password:
        :param confirmpassword:
        :param gender:
        :param usertype:
        :return: post request
        """

        return self.client.post(reverse('signup'), {
            "username": username,
            "password": password,
            "email": email,
            "confirmpassword": confirmpassword,
            "gender": gender,
            "userType": usertype
        })

    def _get_activation_code(self):
        """
        testing if verification code is sent in the email the right way
        :return:
        """
        if len(mail.outbox)==0:
            return ""
        email_body = mail.outbox[-1].body

        match = re.search(r'Your verification code is: (\w+)', email_body)
        if match:
            return int(match.group(1))
        return ""

    def _send_activation_code(self, username, code):

        '''
        this function is testing if assigned verification code is matching with the code inputed

        :param username:
        :param code:
        :return:
        '''

        data = {
            "username": username,
            "verification_code": code
        }

        self.client.post(reverse('verify'), data)

    def test_registration(self):
        """
        testing basic registration functionality with inputed data
        :return:
        """

        self._send_register_request(
            "testuser2",
            "testuser2@example.com",
            "12345",
            "12345",
            "M",
            usertype='basic_user'
        )

        activation_code = self._get_activation_code()

        self._send_activation_code("testuser2", activation_code)

        self.assertTrue(self.User.objects.filter(username='testuser2').exists())

    def test_registration_wrong_activation_code(self):
        """
        testing basic registration functionality with wrong activation code.
        if the code is incorrect than the user cant registrate
        :return:
        """

        self._send_register_request(
            "testuser2",
            "testuser2@example.com",
            "12345",
            "12345",
            "M",
            usertype='basic_user'
        )

        activation_code = self._get_activation_code()

        self._send_activation_code("testuser2", activation_code + 10)

        self.assertFalse(self.User.objects.filter(username='testuser2').exists())

    def test_registration_user_already_exists(self):

        """
        test if a certain user wants to registrate more than once which is not possible
        :return:
        """

        self._send_register_request(
            "testuser1",
            "testuser1@example.com",
            "123456",
            '123456',
            "M",
            'basic_user'
        )

        activation_code = self._get_activation_code()

        self._send_activation_code("testuser1", activation_code)

        self.assertEqual(self.User.objects.get(id=self.user1.id).email, 'testuser1@example.com')

    def test_registration_two_users(self):
        """
        testing basic registration functionality with two users with same data. this
        is irregular scenario
        :return:
        """

        self._send_register_request(
            'testuser2',
            'testuser2@example.com',
            '12345',
            '12345',
            'M',
            'basic_user'
        )

        activation_code1 = self._get_activation_code()

        self._send_register_request(
            'testuser3',
            'testuser3@example.com',
            '12345',
            '12345',
            'M',
            'basic_user'
        )

        activation_code2 = self._get_activation_code()

        self._send_activation_code('testuser2', activation_code1)
        self._send_activation_code('testuser3', activation_code2)

        self.assertTrue(self.User.objects.filter(username='testuser2').exists())
        self.assertTrue(self.User.objects.filter(username='testuser3').exists())



