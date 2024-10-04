"""
Natasa Spasic 2021/0310
"""

import time

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

from nutriplan.my_models.Plan import Plan
from nutriplan.my_tests.SeleniumTest import SeleniumTest

class CommentPlanSeleniumTest(SeleniumTest):
    """
    Class is a Selenium-based test case designed to test the commenting functionality for public plans
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class-level resources for the test suite
        :return:
        """
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up class-level resources after all tests have run
        :return:
        """
        super().tearDownClass()

    def setUp(self):
        """
        Set up the test environment with necessary data and clients
        :return:
        """

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username="testuser1", email="testuser1@example.com", password="12345")

        self.nutri = self.User.objects.create_user(username="nutri", email="nutri@example.com", password="12345")
        self.nutri.groups.add(nutri_group)

        self.plan1 = Plan.objects.create(name="plan1", owner=self.nutri, is_public=True)
        self.plan2 = Plan.objects.create(name="plan2", owner=self.nutri, is_public=False)

    def test_comment(self):
        """
        Test adding a valid comment to a public plan
        :return:
        """

        super().login_user("testuser1", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_plan?plan_id={self.plan1.id}")

        comment_area = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div[1]/textarea')
        comment_area.send_keys("This is a comment")

        send_button = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div[1]/button')
        self.selenium.execute_script("arguments[0].click()", send_button)

        time.sleep(2)

        comments = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]').text

        self.assertTrue("This is a comment" in comments)

    def test_comment_to_long(self):
        """
        Test that an excessively long comment cannot be added to a plan
        :return:
        """
        super().login_user("testuser1", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_plan?plan_id={self.plan1.id}")

        comment_area = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div[1]/textarea')
        comment_area.send_keys("r" * 2000)

        send_button = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div[1]/button')
        self.selenium.execute_script("arguments[0].click()", send_button)

        time.sleep(2)

        comments = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]').text

        self.assertFalse(("r" * 2000) in comments)

