"""
Radovan Jevric 0138/2021
"""

import json

from django.contrib.auth.models import Group
from django.db.models import Avg
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.RatePlan import RatePlan


class RatePlanTest(TestCase):

    """
    Test functionality of rating plan
    """

    def setUp(self):
        """
        Creates 4 users and 2 plans (one public and one not public)
        and 3 users rate plan one will rate in test
        :return:
        """

        self.client = Client()

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model();

        self.user1 = self.User.objects.create_user(username='testuser1', password='12345', email='user1@example.com')
        self.user2 = self.User.objects.create_user(username='testuser2', password='12345', email='user2@example.com')
        self.user3 = self.User.objects.create_user(username='testuser3', password='12345', email='user3@example.com')
        self.user4 = self.User.objects.create_user(username='testuser4', password='12345', email='user4@example.com')

        self.nutri = self.User.objects.create_user(username='nutri', password='12345', email='nutri@example.com')
        self.plan1 = Plan.objects.create(name ="plan1", owner=self.nutri, is_public=True)
        self.plan2 = Plan.objects.create(name ="plan2", owner=self.nutri, is_public=False)

        RatePlan.objects.create(id_user=self.user1, id_plan=self.plan1, score=5)
        RatePlan.objects.create(id_user=self.user2, id_plan=self.plan1, score=1)
        RatePlan.objects.create(id_user=self.user3, id_plan=self.plan1, score=3)

    def _authenticate_user(self, username, password):
        login_successful = self.client.login(username = username, password = password)
        self.assertTrue(login_successful)

    def _send_request(self, plan_id, score):

        self.client.cookies['plan_id'] = plan_id

        data = str(score)

        return self.client.post(reverse('rate-plan'), data=json.dumps(data), content_type='application/json')

    def test_rate_plan(self):
        """
        Normal testing, test if score changed correctly
        :return:
        """

        self._authenticate_user('testuser4', '12345')

        response = self._send_request(self.plan1.id, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(round(response.context['averageScore'], 2), 2.5)
        self.assertEqual(round(RatePlan.objects.filter(id_plan=self.plan1).aggregate(Avg('score'))['score__avg'], 2), 2.5)

    def test_rate_plan_low_score(self):
        """
        Testing if user tries to rate with score -1
        :return:
        """

        self._authenticate_user("testuser4", "12345")

        response = self._send_request(self.plan1.id, -1)

        self.assertNotEqual(response.status_code, 200)

    def test_rate_plan_high_score(self):
        """
        Testing if user tries to rate with score 6
        :return:
        """

        self._authenticate_user("testuser4", "12345")

        response = self._send_request(self.plan1.id, 6)

        self.assertNotEqual(response.status_code, 200)

    def test_user_again(self):
        """
        Testing if user tries to rate same plan 2 times
        the old rate should not be counted
        :return:
        """

        self._authenticate_user('testuser2', '12345')

        response = self._send_request(self.plan1.id, 4)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(round(response.context['averageScore'], 2), 4)
        self.assertEqual(round(RatePlan.objects.filter(id_plan=self.plan1).aggregate(Avg('score'))["score__avg"], 2), 4)


    def test_rate_plan_not_public(self):
        """
        Tests if user tries to rate plan that is not public
        :return:
        """

        self._authenticate_user('testuser3', '12345')

        response = self._send_request(self.plan2.id, 5)

        self.assertNotEqual(response.status_code, 200)


    def test_user_not_authenticated(self):
        """
        User has to be authenticated
        :return:
        """

        response = self._send_request(self.plan1.id, 1)

        self.assertNotEqual(response.status_code, 200)
