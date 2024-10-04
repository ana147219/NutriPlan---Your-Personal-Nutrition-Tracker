'''
Tijana Gasic 0247/2021
'''


import json

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutriplan.my_models.Form import Form
from nutriplan.my_models.Tag import Tag


class FormTest(TestCase):
    """
    this class is testing the basic expected behaviour of the form
    """

    def setUp(self):

        """
        sets the initial data
        :return:
        """

        self.client = Client()

        self.nutri_group = Group.objects.create(name="Nutricionist")

        self.gf_tag = Tag.objects.create(name='gluten free')
        self.vegan_tag = Tag.objects.create(name='vegan')
        self.cd_tag = Tag.objects.create(name='calorie deficit')
        self.kdp_tag = Tag.objects.create(name="keto diet plan")
        self.lcp_tag = Tag.objects.create(name="low calorie plan")
        self.hpp_tag = Tag.objects.create(name="high protein plan")

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username='testuser1', email='testuser1@example.com', password='12345')
        self.user2 = self.User.objects.create_user(username='testuser2', email='testuser2@example.com', password='12345')

        self.nutri = self.User.objects.create_user(username='nutri', email='nutri@example.com', password='12345')
        self.nutri.groups.add(self.nutri_group)

    def _authenticate_user(self):
        login_successful = self.client.login(username='testuser1', password='12345')
        self.assertTrue(login_successful)

    def _send_request(self, id_nutri, height, weight, tags, description):

        """
        sent simple post request
        :param id_nutri:
        :param height:
        :param weight:
        :param tags:
        :param description:
        :return:
        """

        data = {
            "height": height,
            "weight": weight,
            "description": description
        }

        data.update({key: "" for key in tags})

        url = reverse("order_form", args=[id_nutri])

        return self.client.post(url, data=data)

    def test_order_from(self):

        '''
        this function is testing if a form i ordered in a correct way with
        custom text
        :return:
        '''

        self._authenticate_user()

        response = self._send_request(self.nutri.id, 180.0, 75.0, ["gluten_free", "vegan"], "Hocu da mi se napravi neki plan")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Form.objects.filter(
            id_nutritionist=self.nutri,
            height__exact=180,
            weight__exact=75,
            description="Hocu da mi se napravi neki plan",
            tags__in=[self.gf_tag, self.vegan_tag]
        ).exists())

    def test_order_non_nutritionist(self):

        """
        testing to see what happens when form is not ordered from nutritionist
        :return:
        """

        self._authenticate_user()

        response = self._send_request(self.user2.id, 180.0, 75.0, ["gluten_free", "vegan"], "Treba mi plan")

        self.assertEqual(response.status_code, 403)

    def test_non_authenticated(self):
        '''
        testing to see what happens if non authenticated user orders form
        :return:
        '''

        response = self._send_request(self.nutri.id, 180.0, 75.0, ["gluten_free", "vegan"], "Hocu da mi se napravi neki plan")

        self.assertFalse(Form.objects.filter(
            id_nutritionist=self.nutri,
            height__exact=180,
            weight__exact=75,
            description="Hocu da mi se napravi neki plan",
            tags__in=[self.gf_tag, self.vegan_tag]
        ).exists())

    def test_too_long_description(self):

        """
        testing to see what happens when the input text is too long
        :return: bool
        """

        self._authenticate_user()

        response = self._send_request(self.nutri.id, 180.0, 75.0, ["gluten_free", "vegan"], "r"*10000)

        self.assertNotEqual(response, 302)

    def test_bad_height_format(self):

        '''
        testing to see what happens if the incorect format of the data is inputed in the form fields
        :return:
        '''

        self._authenticate_user()

        response = self._send_request(self.nutri.id, "ffff", 75.0, ["gluten_free", "vegan"], "Desc")

        self.assertNotEqual(response, 302)



