"""
Ana Vitkovic 2021/0285
"""

import json

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutriplan.my_models.Day import Day
from nutriplan.my_models.FollowingPlan import FollowingPlan
from nutriplan.my_models.Food import Food
from nutriplan.my_models.Plan import Plan


class PlanTests(TestCase):

    def setUp(self):
        """
        This method sets up the test environment, creating a test client, users, food item, plans, days, and following plans, preparing the necessary data for the test cases.
        :return:
        """

        self.client = Client()

        self.User = get_user_model()
        nutri_group = Group.objects.create(name='Nutricionist')

        self.food1 = Food.objects.create(name="Lime", food_type="vg", calories=100, protein=2, carbs=2, fiber=2, fat=2,
                                         sugar=2, unit="g")

        self.user1 = self.User.objects.create_user(username='testuser1', email='testuser1@example.com', password='12345')
        self.user2 = self.User.objects.create_user(username='testuser2', email='testuser2@example.com', password='12345')
        self.user3 = self.User.objects.create_user(username='testuser3', email='testuser3@example.com', password='12345')

        self.nutri = self.User.objects.create_user(username='nutri', email='nutri', password='12345')
        self.nutri.groups.add(nutri_group)

        self.plan1 = Plan.objects.create(name="plan1", owner=self.user1, is_public=False)
        Day.objects.create(plan=self.plan1, day_number=1)
        self.plan2 = Plan.objects.create(name="plan2", owner=self.nutri, is_public=False)
        Day.objects.create(plan=self.plan2, day_number=1)

        FollowingPlan.objects.create(id_plan=self.plan2, id_user=self.user1)

    def _authenticate_user(self, username, password):
        """
        Authenticates the test client with the provided username and password. Ensures the user is logged in before performing actions.
        :return:
        """
        login_successful = self.client.login(username=username, password=password)
        self.assertTrue(login_successful)

    def _send_make_plan_request(self):
        """
        Sends a POST request to the server to create a new plan.
        It uses the Django test client's post method to send a request to the URL that corresponds to the named URL pattern "make_plan".
        :return: response received from the server after sending the POST request
        """
        return self.client.post(reverse("make_plan"))

    def _change_plan_request(self, new_name, tags, days, plan_id):
        """
        Changes the plan's name, tags, and days by sending a POST request with the new data.
        :param new_name:
        :param tags:
        :param days:
        :param plan_id:
        :return: response received from the server after sending the POST request
        """
        self.client.cookies["plan_id"] = plan_id

        data = {
            "name": new_name,
            "tags": tags,
            "days": days
        }

        return self.client.post(reverse("save-plan"), data=json.dumps(data), content_type="application/json")

    def _get_empty_day(self):
        """
        :return: Returns a dictionary representing an empty day with 24 hours, each hour containing an empty list.
        """
        return {"{:02d}:00".format(hour): [] for hour in range(0, 24)}

    def _get_day_invalid(self):
        """
        :return:Returns a dictionary representing a day with 24 hours, where the 10:00 hour has an invalid food entry.
        """
        day = {"{:02d}:00".format(hour): [] for hour in range(0, 24)}

        day["10:00"] = [{"img": "", "amount": -20, "food_id": self.food1.id}]

        return day

    def test_create_plan(self):
        """
        Authenticates a user and tests creating a plan, expecting a redirection status code (302).
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._send_make_plan_request()

        self.assertEqual(response.status_code, 302)

    def test_change_plan_name(self):
        """
        Tests changing the name of a plan, expecting a successful response (status code 201).
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._change_plan_request("plan1", [], {"Day 1": self._get_empty_day()}, self.plan1.id)

        self.assertEqual(response.status_code, 201)

    def test_change_plan_other_plan(self):
        """
        Tests changing a plan by a user who doesn't own it, expecting a failure (status code not 201).
        :return:
        """
        self._authenticate_user("testuser2", "12345")

        response = self._change_plan_request("plan1", [], {"Day 1": self._get_empty_day()}, self.plan1.id)

        self.assertNotEqual(response.status_code, 201)

    def test_change_plan_name_too_long(self):
        """
        Tests changing a plan with a name that's too long, expecting a failure (status code not 201).
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._change_plan_request("r" * 1000, [], {"Day 1": self._get_empty_day()}, self.plan1.id)

        self.assertNotEqual(response.status_code, 201)

    def test_change_plan_bad_parameters(self):
        """
        Tests changing a plan with invalid parameters (days set to None), expecting a failure (status code not 201).
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._change_plan_request("plan1", [], None, self.plan1.id)

        self.assertNotEqual(response.status_code, 201);

    def test_change_plan_invalid_food(self):
        """
        Tests changing a plan with invalid food data, expecting a failure (status code not 201).
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._change_plan_request("plan1", [], {"Day 1": self._get_day_invalid()}, self.plan1.id)

        self.assertNotEqual(response.status_code, 201)

    def test_change_plan_not_owner(self):
        """
        Tests changing a plan by a user who doesn't own it, expecting a failure (status code not 201).
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._change_plan_request("plan2", [], {"Day 1": self._get_empty_day()}, self.plan2.id)

        self.assertNotEqual(response.status_code, 201)

    def _send_plan_to_someone_request(self, plan_id, username):
        """
        Sends a plan to another user by sending a POST request with the plan ID and recipient username.
        :param plan_id:
        :param username:
        :return:
        """

        data = {
            "plan_id": plan_id,
            "user_sending": username
        }

        return self.client.post(reverse("send-plan"), data=json.dumps(data), content_type="application/json")



    def test_send_plan(self):
        """
        Tests sending a plan to another user, expecting a successful response (status code 201) and a FollowingPlan record.
        :return:
        """

        self._authenticate_user("testuser1", "12345")

        response = self._send_plan_to_someone_request(self.plan1.id, self.user2.username)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(FollowingPlan.objects.filter(id_user=self.user2, id_plan=self.plan1).exists())

    def test_send_plan_not_owner(self):
        """
        Tests sending a plan by a user who doesn't own it, expecting a failure (status code not 201) and no FollowingPlan record.
        :return:
        """

        self._authenticate_user("testuser1", "12345")

        response = self._send_plan_to_someone_request(self.plan2.id, self.user2.username)

        self.assertNotEqual(response.status_code, 201)
        self.assertFalse(FollowingPlan.objects.filter(id_user=self.user2, id_plan=self.plan1).exists())

    def test_send_plan_user_not_exist(self):
        """
        Tests sending a plan to a non-existent user, expecting a failure (status code not 201) and no FollowingPlan record.
        :return:
        """
        self._authenticate_user("testuser1", "12345")

        response = self._send_plan_to_someone_request(self.plan2.id, "Ne postoji korisnik")

        self.assertNotEqual(response.status_code, 201)
        self.assertFalse(FollowingPlan.objects.filter(id_user=self.user2, id_plan=self.plan1).exists())

    def _publish_plan(self, id_plan):
        """
        Publishes a plan by sending a POST request with the plan ID and state.
        :param id_plan:
        :return:
        """

        data = {
            "plan_id": id_plan,
            "state": True
        }

        return self.client.post(reverse("publish-plan"), data=json.dumps(data), content_type="application/json")

    def test_publish_plan(self):
        """
        Tests publishing a plan, expecting a successful response (status code 200) and the plan to be marked as public.
        :return:
        """

        self._authenticate_user("nutri", "12345")

        response = self._publish_plan(self.plan2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Plan.objects.get(id=self.plan2.id).is_public, True)

    def test_publish_plan_not_owner(self):
        """
        Tests publishing a plan by a user who doesn't own it, expecting a failure (status code not 200) and the plan to remain non-public.
        :return:
        """

        self._authenticate_user("testuser1", "12345")

        response = self._publish_plan(self.plan2.id)

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Plan.objects.get(id=self.plan2.id).is_public, False)

    def _begin_plan(self, plan_id):
        """
        Begins a plan by sending a POST request with the plan ID.
        :param plan_id:
        :return:
        """

        self.client.cookies["plan_id"] = plan_id

        return self.client.post(reverse("begin-plan"))

    def test_begin_plan(self):
        """
        Tests beginning a plan, expecting a successful response (status code 201).
        :return:
        """

        self._authenticate_user("testuser1", "12345")

        response = self._begin_plan(self.plan2.id)

        self.assertEqual(response.status_code, 201)

    def test_begin_two_plan(self):
        """
        Tests beginning two plans in succession, expecting the first to succeed (status code 201) and the second to fail (status code not 201).
        :return:
        """

        self._authenticate_user("testuser1", "12345")

        response1 = self._begin_plan(self.plan2.id)

        response2 = self._begin_plan(self.plan1.id)

        self.assertEqual(response1.status_code, 201)
        self.assertNotEqual(response2.status_code, 201)





