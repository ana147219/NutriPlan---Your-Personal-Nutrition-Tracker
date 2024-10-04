"""
Radovan Jevric 0138/2021
"""

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlencode

class SearchNutriTest(TestCase):
    """
    Class provides testing basic functionality for searching nutritions
    """

    def setUp(self):
        """
        We create one user that will seacrch
        and two users that will be searched
        :return:
        """

        self.client = Client()

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()
        self.user1 = self.User.objects.create_user('testuser1', 'user1@example', '12345')
        self.user2 = self.User.objects.create_user('testuser2', 'user2@example', '12345')
        self.user2.groups.add(nutri_group)
        self.user3 = self.User.objects.create_user('testuser3', 'user3@example', '12345')
        self.user3.groups.add(nutri_group)

    def _authenticate_user(self):
        """
        We need to authenticate user before doing anything
        :return:
        """
        login_successful = self.client.login(username='testuser1', password='12345')
        self.assertTrue(login_successful)

    def _send_request(self, name, ordering):
        """
        Make data from reuqeust and send it to server with post request
        :param name:
        :param ordering:
        :return:
        """
        url = reverse('get-nutri-list')

        params = {
            'search-input': name,
            'order': ordering,
        }

        query_string = urlencode(params)

        full_url = f'{url}?{query_string}'

        return self.client.get(full_url)

    def test_search_nutri_name(self):
        """
        Functionality testing basic functionality for searching nutritions
        it needs to get two nutritionist, but first user should not be displayed
        because he is not nutritionist
        :return:
        """

        self._authenticate_user()
        response = self._send_request('testuser2', 'alphabeticalASC')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2, response.context["nutris"])
        self.assertNotIn(self.user3, response.context["nutris"])
        self.assertNotIn(self.user1, response.context["nutris"])

    def test_search_non_nutri(self):
        """
        Searching only first user result should be empty
        :return:
        """

        self._authenticate_user()
        response = self._send_request("testuser1", "alphabeticalASC")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["empty"], 0)

    def test_search_non_authenticated(self):
        """
        Trying to search when we are not authenticated
        we should be redirect to login page
        :return:
        """

        response = self._send_request("testuser1", "alphabeticalASC")

        self.assertNotEqual(response.status_code, 200)

