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
from nutriplan.my_models.RateNutri import RateNutri
from nutriplan.my_models.RatePlan import RatePlan


class RateNutriTest(TestCase):

    def setUp(self):
        """
        Creates 4 users that will give grades, and one additional that will give new grade
        and 1 nutritionist that will be rated
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
        self.nutri.groups.add(nutri_group)

        RateNutri.objects.create(id_user=self.user1, id_nutricionist=self.nutri, score=5)
        RateNutri.objects.create(id_user=self.user2, id_nutricionist=self.nutri, score=1)
        RateNutri.objects.create(id_user=self.user3, id_nutricionist=self.nutri, score=3)

    def _authenticate_user(self, username, password):
        login_successful = self.client.login(username=username, password=password)
        self.assertTrue(login_successful)

    def _send_request(self, nutri_id, score):

        self.client.cookies['nutri_id'] = nutri_id

        data = str(score)

        return self.client.post(reverse('rate-nutri'), data=json.dumps(data), content_type='application/json')

    def test_rate_nutri(self):
        """
        Normal test, it needs to check if grades changes to some other value
        :return:
        """

        self._authenticate_user('testuser4', '12345')

        response = self._send_request(self.nutri.id, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(round(response.context['averageScore'], 2), 2.5)
        self.assertEqual(round(RateNutri.objects.filter(id_nutricionist=self.nutri).aggregate(Avg('score'))['score__avg'], 2), 2.5)

    def test_rate_nutri_low_score(self):
        """
        It tests if somebody gives score that is less than 0
        :return:
        """

        self._authenticate_user("testuser4", "12345")

        response = self._send_request(self.nutri.id, -1)

        self.assertNotEqual(response.status_code, 200)

    def test_rate_nutri_high_score(self):
        """
        It tests when somebody gives score that is greater than 5
        :return:
        """

        self._authenticate_user("testuser4", "12345")

        response = self._send_request(self.nutri.id, 6)

        self.assertNotEqual(response.status_code, 200)

    def test_user_again(self):
        """
        Tests if user tries again to rate some nutritionits
        the old score should not be counted
        :return:
        """

        self._authenticate_user('testuser2', '12345')

        response = self._send_request(self.nutri.id, 4)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(round(response.context['averageScore'], 2), 4)
        self.assertEqual(round(RateNutri.objects.filter(id_nutricionist=self.nutri).aggregate(Avg('score'))["score__avg"], 2), 4)

    def test_rate_non_nutritionist(self):
        """
        Test should not rate nutritionist
        and it should not return status code 200
        :return:
        """

        self._authenticate_user('testuser4', '12345')

        response = self._send_request(self.user2.id, 1)

        self.assertNotEqual(response.status_code, 200)

    def test_user_not_authenticated(self):
        """
        User has to be authenticated
        :return:
        """

        response = self._send_request(self.nutri.id, 1)

        self.assertNotEqual(response.status_code, 200)
