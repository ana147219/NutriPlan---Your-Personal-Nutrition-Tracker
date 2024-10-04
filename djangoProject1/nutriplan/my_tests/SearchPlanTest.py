"""
Radovan Jevric 0138/2021
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from urllib.parse import urlencode

from nutriplan.my_models.Day import Day
from nutriplan.my_models.HasTag import HasTag
from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.Tag import Tag


class SearchPlanTest(TestCase):
    """
    Class provides tests for searching plans
    """

    def setUp(self):
        """
        We create tags, and we setup, make some plans and add tags and
        days to them
        :return:
        """
        self.client = Client()

        gf_tag = Tag.objects.create(name='gluten free')
        vegan_tag = Tag.objects.create(name='vegan')
        cd_tag = Tag.objects.create(name='calorie deficit')
        kdp_tag = Tag.objects.create(name="keto diet plan")
        lcp_tag = Tag.objects.create(name="low calorie plan")
        hpp_tag = Tag.objects.create(name="high protein plan")

        self.User = get_user_model()
        user1 = self.User.objects.create_user(username='testuser', password='12345')

        self.plan1 = Plan.objects.create(name="plan1", owner=user1, is_public=True)
        HasTag.objects.create(tag=gf_tag, plan=self.plan1)
        HasTag.objects.create(tag=vegan_tag, plan=self.plan1)
        Day.objects.create(plan=self.plan1, day_number=1)
        Day.objects.create(plan=self.plan1, day_number=2)
        Day.objects.create(plan=self.plan1, day_number=3)
        Day.objects.create(plan=self.plan1, day_number=4)
        Day.objects.create(plan=self.plan1, day_number=5)

        self.plan2 = Plan.objects.create(name="plan2", owner=user1, is_public=False)
        HasTag.objects.create(tag=vegan_tag, plan=self.plan2)
        Day.objects.create(plan=self.plan2, day_number=1)

        self.plan3 = Plan.objects.create(name="plan3", owner=user1, is_public=True)
        HasTag.objects.create(tag=vegan_tag, plan=self.plan3)
        Day.objects.create(plan=self.plan3, day_number=1)
        Day.objects.create(plan=self.plan3, day_number=2)


    def _autentcate_user(self):
        """
        User has to be authenticated
        :return:
        """
        login_successful = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_successful)

    def _send_request(self, name, days_num, include_days, filters):
        """
        Packs parameter in request data and sends post request
        :param name: plan_name
        :param days_num: number of days
        :param include_days: do we have to include number of days
        :param filters: did user put some tag filters
        :return:
        """
        url = reverse('get-plan-list')

        params = {
            "search-input": name,
            "days": days_num,
            "include-days": include_days,
            "order": "alphabeticalASC",
            "filters": filters
        }

        query_string = urlencode(params)

        full_url = f'{url}?{query_string}'

        return self.client.get(full_url)

    def test_search_non_public(self):
        """
        Test for searching a plan that is not public
        it should not return anything
        :return:
        """

        self._autentcate_user()
        response = self._send_request('plan2', 1, 0, [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["empty"], 0)

    def test_search_plan_name(self):
        """
        Searching a plan by name it should return all
        public plans
        :return:
        """
        self._autentcate_user()
        response = self._send_request("pla", 0, 0, "")

        plans = [d["plan"] for d in response.context["plansAndTags"] if "plan" in d]

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.plan3, plans)
        self.assertIn(self.plan1, plans)
        self.assertNotIn(self.plan2, plans)

    def test_search_plan_not_authenticated(self):
        """
        User has to be authenticated, so it
        cannot return 200 status code
        :return:
        """

        response = self._send_request("pla", 0, 0, "")

        self.assertNotEqual(response.status_code, 200)

    def test_search_plan_days(self):
        """
        Testing for searching a plan but filtered
        by days
        :return:
        """

        self._autentcate_user()
        response = self._send_request("", 4, 1, "")


        plans = [d["plan"] for d in response.context["plansAndTags"] if "plan" in d]

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.plan1, plans)
        self.assertNotIn(self.plan2, plans)
        self.assertIn(self.plan3, plans)

    def test_search_plan_filters(self):
        """
        Testing for searching a plan with tag
        filters
        :return:
        """

        self._autentcate_user()
        response = self._send_request("", 0, 0, "gluten free,vegan")


        plans = [d["plan"] for d in response.context["plansAndTags"] if "plan" in d]


        self.assertEqual(response.status_code, 200)
        self.assertIn(self.plan1, plans)
        self.assertNotIn(self.plan2, plans)
        self.assertNotIn(self.plan3, plans)

    def test_search_plan_nothing(self):
        """
        Searching plan by name nothing should be returned
        :return:
        """

        self._autentcate_user()
        response = self._send_request("plan_that_does_not_exist", 0, 0, [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["empty"], 0)

    def test_search_plan_filter_union(self):
        """
        Test for searching plans that both have that tag
        2 plans should be returned
        :return:
        """
        self._autentcate_user()
        response = self._send_request("", 0, 0,"vegan")

        plans = [d["plan"] for d in response.context["plansAndTags"] if "plan" in d]

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.plan1, plans)
        self.assertNotIn(self.plan2, plans)
        self.assertIn(self.plan3, plans)


