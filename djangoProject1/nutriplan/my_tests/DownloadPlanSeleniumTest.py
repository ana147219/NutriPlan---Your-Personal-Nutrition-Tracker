"""
Radovan Jevric 0138/2021
"""
import time

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

from nutriplan.my_models.Day import Day
from nutriplan.my_models.FollowingPlan import FollowingPlan
from nutriplan.my_models.Plan import Plan
from nutriplan.my_tests.SeleniumTest import SeleniumTest

class DownloadPlanSeleniumTest(SeleniumTest):

    """
    Class runs webdriver to test downloading plan functionality.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


    def setUp(self):
        """
        Creates one user and one nutritionist
        that owns one plan
        :return:
        """

        nutri_group = Group.objects.create(name='Nutricionist')

        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', email='user@example.com', password='12345')

        self.nutri = self.User.objects.create_user(username='nutri', email='nutri@example.com', password='12345')
        self.nutri.groups.add(nutri_group)

        self.plan1 = Plan.objects.create(name='plan1', owner=self.nutri, is_public=True)
        Day.objects.create(day_number=1, plan=self.plan1)

        self.plan2 = Plan.objects.create(name='plan2', owner=self.nutri, is_public=False)
        Day.objects.create(day_number=1, plan=self.plan2)

    def test_download(self):
        """
        Testing if test is downloaded again and check
        if user can see that plan in his plans
        :return:
        """

        super().login_user(self.user.username, "12345")

        self.selenium.get(f"{self.live_server_url}/preview_plan?plan_id={self.plan1.id}")

        download_button = self.selenium.find_element(By.XPATH, '//*[@id="download_plan_btn"]')
        self.selenium.execute_script("arguments[0].click()", download_button)

        try:
            self.selenium.find_element(By.CLASS_NAME, 'success-col')
            self.selenium.implicitly_wait(10)

            self.selenium.get(f"{self.live_server_url}/home")

            plans = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[2]/div').text
            self.assertTrue(self.plan1.name in plans)

        except NoSuchElementException:
            self.assertTrue(False)

    def test_download_again(self):
        """
        Checks what happens when downloading plan again
        and user should still see only one plan
        :return:
        """

        FollowingPlan.objects.create(id_plan=self.plan1, id_user=self.user)

        super().login_user(self.user.username, "12345")

        self.selenium.get(f"{self.live_server_url}/preview_plan?plan_id={self.plan1.id}")

        download_button = self.selenium.find_element(By.XPATH, '//*[@id="download_plan_btn"]')
        self.selenium.execute_script("arguments[0].click()", download_button)

        try:
            self.selenium.find_element(By.CLASS_NAME, 'warning-col')
            self.selenium.implicitly_wait(10)

            self.selenium.get(f"{self.live_server_url}/home")

            plans = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[2]/div').text
            self.assertTrue(self.plan1.name in plans)

        except NoSuchElementException:
            self.assertTrue(False)