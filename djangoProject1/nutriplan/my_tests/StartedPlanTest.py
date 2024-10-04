"""
Ana Vitkovic 2021/0285
"""

import json
from datetime import datetime, date

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutriplan.my_models.Day import Day
from nutriplan.my_models.DayHistory import DayHistory
from nutriplan.my_models.Food import Food
from nutriplan.my_models.Meal import Meal
from nutriplan.my_models.MealStatus import MealStatus
from nutriplan.my_models.MealsInDay import MealsInDay
from nutriplan.my_models.Plan import Plan


class StartedPlanTest(TestCase):

    def setUp(self):

        """
        This method sets up the test environment.
        It creates a test client, user, food item, plan, day, meals, and meal statuses, preparing the necessary data for the test cases.
        :return:
        """

        self.client = Client()

        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="testuser1", password="12345", email="testuser1@example.com")

        self.food1 = Food.objects.create(name="Lime", food_type="vg", calories=100, protein=2, carbs=2, fiber=2, fat=2,
                                         sugar=2, unit="g")

        self.plan1 = Plan.objects.create(name="plan1", owner=self.user, is_public=False)
        self.day1 = Day.objects.create(plan=self.plan1, day_number=1)

        self.meal1 = Meal.objects.create(food=self.food1, amount=100, hour=datetime.now().hour)

        if (datetime.now().hour < 23): other_hour = datetime.now().hour + 1
        else: other_hour = datetime.now().hour - 1
        self.meal2 = Meal.objects.create(food=self.food1, amount=100, hour=other_hour)

        MealsInDay.objects.create(day=self.day1, meal=self.meal1)
        MealsInDay.objects.create(day=self.day1, meal=self.meal2)

        self.date_day = DayHistory.objects.create(user=self.user, plan_index=self.plan1.id, data=date.today())
        self.meal_status1 = MealStatus.objects.create(meal=self.meal1, day_history=self.date_day, status=False)
        self.meal_status2= MealStatus.objects.create(meal=self.meal2, day_history=self.date_day, status=False)

    def _authenticate(self):
        """
        Authenticates the test client with the credentials of testuser1. Ensures the user is logged in before performing actions.
        :return:
        """
        login_successful = self.client.login(username="testuser1", password="12345")
        self.assertTrue(login_successful)

    def _send_request(self, meal_id):
        """
        Sends a POST request to the finish-meal endpoint with the given meal ID in the request data.
        :param meal_id:
        :return:
        """
        data = {
            "id": meal_id
        }

        return self.client.post(reverse("finish-meal"), data=json.dumps(data), content_type="application/json")

    def test_finish_meal(self):
        """
        Authenticates the user, sends a request to finish a meal (meal_status1), and asserts that the response status is 200 and the meal status is updated to True.
        :return:
        """

        self._authenticate()

        response = self._send_request(self.meal_status1.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(MealStatus.objects.get(id=self.meal_status1.id).status, True)

    def test_finish_meal_not_time(self):
        """
        Authenticates the user, sends a request to finish a meal (meal_status2) that's not supposed to be finished at the current time,
        and asserts that the response status is not 200 and the meal status remains False.
        :return:
        """

        self._authenticate()

        response = self._send_request(self.meal_status2.id)

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(MealStatus.objects.get(id=self.meal_status2.id).status, False)

    def test_finish_meal_twice(self):
        """
        Authenticates the user, sends requests to finish two meals (meal_status1 and meal_status2).
        This test doesn't have assertions but is meant to test the behavior when finishing multiple meals.
        :return:
        """

        self._authenticate()

        self._send_request(self.meal_status1.id)
        self._send_request(self.meal_status2.id)

    def test_finish_meal_not_found(self):
        """
        Authenticates the user, sends a request to finish a non-existent meal (by using an ID far beyond the existing ones),
        git status
        testing the behavior when the meal ID is invalid.
        :return:
        """

        self._authenticate()

        self._send_request(self.meal_status2.id + 100)


