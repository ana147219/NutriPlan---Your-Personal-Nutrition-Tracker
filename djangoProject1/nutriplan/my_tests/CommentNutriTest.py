"""
Natasa Spasic 2021/0310
"""

import json

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutriplan.my_models.NutriComment import NutriComment


class CommentNutriTest(TestCase):
    """
    Class for testing the commenting functionality for nutritionists
    """

    def setUp(self):
        """
        Set up the test environment with necessary data and clients
        :return:
        """
        self.client = Client()

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username="testuser1", email="testuser1@example.com",
                                                   password="12345")
        self.user2 = self.User.objects.create_user(username="testuser2", email="testuser2@example.com",
                                                   password="12345")

        self.nutri = self.User.objects.create_user(username="nutri", email="nutri@example.com", password="12345")
        self.nutri.groups.add(nutri_group)

    def _authenticate_user(self):
        """
        Log in as the test user and check that login was successful
        :return:
        """
        login_successful = self.client.login(username="testuser1", password="12345")
        self.assertTrue(login_successful)

    def _send_request(self, nutri_id, text):
        """
        Send a POST request to add a comment with the given nutritionist ID and text
        :param nutri_id:
        :param text:
        :return: response received from the server after sending the POST request
        """
        self.client.cookies["nutri_id"] = nutri_id

        data = {
            "text": text
        }

        return self.client.post(reverse('add_comment_nutri'), data=json.dumps(data), content_type="application/json")

    def test_comment_nutri(self):
        """
        Test that a comment can be successfully added by an authenticated user
        :return:
        """
        self._authenticate_user()

        response = self._send_request(self.nutri.id, "Ovo je neki komentar")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(NutriComment.objects.filter(nutri=self.nutri, text__exact="Ovo je neki komentar").exists())

    def test_comment_not_nutri(self):
        """
        Test that a comment cannot be added if the user is not a nutritionist
        :return:
        """
        self._authenticate_user()

        response = self._send_request(self.user2.id, "Ovo je neki komentar")

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(NutriComment.objects.filter(nutri=self.nutri, text__exact="Ovo je neki komentar").exists())

    def test_comment_to_long(self):
        """
        Test that a comment that is too long cannot be added
        :return:
        """
        self._authenticate_user()

        response = self._send_request(self.nutri.id, "r" * 1000000)

        self.assertNotEqual(response.status_code, 200)

    def test_comment_no_auth(self):
        """
        Test that a comment cannot be added without authentication
        :return:
        """
        response = self._send_request(self.nutri.id, "Ovo je neki komentar")

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(NutriComment.objects.filter(nutri=self.nutri, text__exact="Ovo je neki komentar").exists())
