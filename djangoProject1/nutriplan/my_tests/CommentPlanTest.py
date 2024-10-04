"""
Natasa Spasic 2021/0310
"""

import json

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.PlanComment import PlanComment


class CommentPlanTest(TestCase):
    """
    Class for testing the commenting functionality for public plans
    """
    def setUp(self):
        """
        Set up the test environment with necessary data and clients
        :return:
        """

        self.client = Client()

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username="testuser1", email="testuser1@example.com", password="12345")

        self.nutri = self.User.objects.create_user(username="nutri", email="nutri@example.com", password="12345")
        self.nutri.groups.add(nutri_group)

        self.plan1 = Plan.objects.create(name="plan1", owner=self.nutri, is_public=True)
        self.plan2 = Plan.objects.create(name="plan2", owner=self.nutri, is_public=False)

    def _authenticate_user(self):
        """
        Log in as the test user and check that login was successful
        :return:
        """
        login_successful = self.client.login(username="testuser1", password="12345")
        self.assertTrue(login_successful)

    def _send_request(self, plan_id, text):
        """
        Send a POST request to add a comment with the given plan ID and text
        :param plan_id:
        :param text:
        :return: response received from the server after sending the POST request
        """
        self.client.cookies["plan_id"] = plan_id

        data = {
           "text": text
        }

        return self.client.post(reverse('add_comment_plan'), data=json.dumps(data), content_type="application/json")

    def test_comment_plan(self):
        """
        Test that a comment can be successfully added to a public plan
        :return:
        """

        self._authenticate_user()

        response = self._send_request(self.plan1.id, "Ovo je neki komentar")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(PlanComment.objects.filter(plan=self.plan1, text__exact="Ovo je neki komentar").exists())

    def test_comment_plan_not_public(self):
        """
        Test that a comment cannot be added to a non-public plan
        :return:
        """

        self._authenticate_user()

        response = self._send_request(self.plan2.id, "Ovo je neki komentar")

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(PlanComment.objects.filter(plan=self.plan1, text__exact="Ovo je neki komentar").exists())

    def test_comment_to_long(self):
        """
        Test that a comment that is too long cannot be added
        :return:
        """

        self._authenticate_user()

        response = self._send_request(self.plan1.id, "r" * 1000000)

        self.assertNotEqual(response.status_code, 200)

    def test_comment_no_auth(self):
        """
        Test that a comment cannot be added without authentication
        :return:
        """

        response = self._send_request(self.plan1.id, "Ovo je neki komentar")

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(PlanComment.objects.filter(plan=self.plan1, text__exact="Ovo je neki komentar").exists())
