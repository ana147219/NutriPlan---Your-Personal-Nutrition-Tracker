"""
Radovan Jevric 0138/2021
"""
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutriplan.my_models.Day import Day
from nutriplan.my_models.FollowingPlan import FollowingPlan
from nutriplan.my_models.Plan import Plan


class DownloadPlanTest(TestCase):

    """
    Tests for users that try to download plan
    """

    def setUp(self):
        """
        Creates one user, and one nutri that has plan
        :return:
        """

        self.client = Client()

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', email='user@example.com', password='12345')

        self.nutri = self.User.objects.create_user(username='nutri', email='nutri@example.com', password='12345')
        self.nutri.groups.add(nutri_group)

        self.plan1 = Plan.objects.create(name='plan1', owner=self.nutri, is_public=True)
        Day.objects.create(day_number=1, plan=self.plan1)

        self.plan2 = Plan.objects.create(name='plan2', owner=self.nutri, is_public=False)
        Day.objects.create(day_number=1, plan=self.plan2)

    def _authenticate_user(self):
        login_success = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_success)

    def _send_request(self, plan_id):

        self.client.cookies["plan_id"] = plan_id

        return self.client.post(reverse("download-plan"))


    def test_download_plan(self):
        """
        Normal test for downloading the plan
        user should see that plan when he dowmloaded it
        :return:
        """

        self._authenticate_user()
        response = self._send_request(self.plan1.id)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.plan1, Plan.objects.filter(followingplan__id_user=self.user))

    def test_download_non_public_plan(self):
        """
        When user tries to download plan that is not public, it
        should not be seen in his plans
        :return:
        """
        self._authenticate_user()
        response = self._send_request(self.plan2.id)

        self.assertEqual(response.status_code, 403)

    def test_download_non_authenticated(self):
        """
        User has to be authenticated
        :return:
        """

        response = self._send_request(self.plan1.id)

        self.assertNotEqual(response.status_code, 200)

