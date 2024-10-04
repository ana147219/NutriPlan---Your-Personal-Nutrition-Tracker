"""
Natasa Spasic 2021/0310
"""

import time

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

from nutriplan.my_tests.SeleniumTest import SeleniumTest


class CommentNutriSeleniumTest(SeleniumTest):
    """
    Class is a Selenium-based test case designed to test the commenting functionality for nutritionists
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

        self.user1 = self.User.objects.create_user(username="testuser1", email="testuser1@example.com",
                                                   password="12345")
        self.user2 = self.User.objects.create_user(username="testuser2", email="testuser2@example.com",
                                                   password="12345")

        self.nutri = self.User.objects.create_user(username="nutri", email="nutri@example.com", password="12345")
        self.nutri.groups.add(nutri_group)

    def test_comment(self):
        """
        Test adding a valid comment to a nutritionist profile
        :return:
        """

        super().login_user("testuser1", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_nutri?nutri_id={self.nutri.id}")

        comment_area = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/textarea')
        comment_area.send_keys("This is a comment")

        send_button = self.selenium.find_element(By.XPATH, '//*[@id="submit_com_nutri"]')
        self.selenium.execute_script("arguments[0].click()", send_button)

        time.sleep(2)

        comments = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]').text

        self.assertTrue("This is a comment" in comments)

    def test_comment_to_long(self):
        """
        Test that an excessively long comment cannot be added
        :return:
        """
        super().login_user("testuser1", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_nutri?nutri_id={self.nutri.id}")

        comment_area = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/textarea')
        comment_area.send_keys("r" * 2000)

        send_button = self.selenium.find_element(By.XPATH, '//*[@id="submit_com_nutri"]')
        self.selenium.execute_script("arguments[0].click()", send_button)

        time.sleep(2)

        comments = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[2]').text

        self.assertFalse(("r" * 2000) in comments)



