"""
Radovan Jevric 0138/2021
"""

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.RatePlan import RatePlan
from nutriplan.my_tests.SeleniumTest import SeleniumTest


class RatePlanSeleniumTest(SeleniumTest):
    """
    Test that check rate plan functionality
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        """
        Creates one nutri and 4 users
        3 of them rated and one that will rate in test
        :return:
        """

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username='testuser1', password='12345', email='user1@example.com')
        self.user2 = self.User.objects.create_user(username='testuser2', password='12345', email='user2@example.com')
        self.user3 = self.User.objects.create_user(username='testuser3', password='12345', email='user3@example.com')
        self.user4 = self.User.objects.create_user(username='testuser4', password='12345', email='user4@example.com')

        self.nutri = self.User.objects.create_user(username='nutri', password='12345', email='nutri@example.com')
        self.nutri.groups.add(nutri_group)
        self.plan1 = Plan.objects.create(name="plan1", owner=self.nutri, is_public=True)
        self.plan2 = Plan.objects.create(name="plan2", owner=self.nutri, is_public=False)

        RatePlan.objects.create(id_user=self.user1, id_plan=self.plan1, score=5)
        RatePlan.objects.create(id_user=self.user2, id_plan=self.plan1, score=1)
        RatePlan.objects.create(id_user=self.user3, id_plan=self.plan1, score=3)

    def test_grade(self):
        """
        Normal test that will check does score change
        when somebody rate
        :return:
        """
        super().login_user("testuser4", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_plan?plan_id={self.plan1.id}")

        rate_button = self.selenium.find_element(By.XPATH, '//*[@id="rate_btn"]')
        self.selenium.execute_script("arguments[0].click()", rate_button)

        star = self.selenium.find_element(By.XPATH, '//*[@id="collapseWidthExample"]/div/div/div/label[5]')
        self.selenium.execute_script("arguments[0].click()", star)

        submit_rate = self.selenium.find_element(By.XPATH, '//*[@id="submit_rate_btn_plan"]')
        self.selenium.execute_script("arguments[0].click()", submit_rate)

        self.selenium.implicitly_wait(10)
        self.selenium.find_element(By.CLASS_NAME, 'success-col')
        grade = self.selenium.find_element(By.XPATH, '//*[@id="averageRating"]').text

        self.assertEqual(grade, '2.5 / 5')

    def test_grade_same_user(self):
        """
        Test that check if some user tried again to rate
        old grade should not be counted
        :return:
        """
        super().login_user("testuser3", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_plan?plan_id={self.plan1.id}")

        rate_button = self.selenium.find_element(By.XPATH, '//*[@id="rate_btn"]')
        self.selenium.execute_script("arguments[0].click()", rate_button)

        star = self.selenium.find_element(By.XPATH, '//*[@id="collapseWidthExample"]/div/div/div/label[2]')
        self.selenium.execute_script("arguments[0].click()", star)

        submit_rate = self.selenium.find_element(By.XPATH, '//*[@id="submit_rate_btn_plan"]')
        self.selenium.execute_script("arguments[0].click()", submit_rate)

        self.selenium.implicitly_wait(10)
        self.selenium.find_element(By.CLASS_NAME, 'success-col')
        grade = self.selenium.find_element(By.XPATH, '//*[@id="averageRating"]').text

        self.assertEqual(grade, '3.33 / 5')


