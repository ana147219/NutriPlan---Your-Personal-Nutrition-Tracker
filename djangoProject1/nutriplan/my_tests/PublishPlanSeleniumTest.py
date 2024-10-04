"""
Ana Vitkovic 2021/0285
"""

from time import sleep

from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

from nutriplan.my_models.FollowingPlan import FollowingPlan
from nutriplan.my_models.Plan import Plan
from nutriplan.my_tests.SeleniumTest import SeleniumTest


class PublishPlanSeleniumTest(SeleniumTest):

    @classmethod
    def setUpClass(cls):
        """
        method is called once before any tests in the class run. It typically sets up state that is shared across tests.
        :return:
        """
        super().setUpClass()

    def setUp(self):
        """
         method is used to set up any state needed for the tests to run
        :return:
        """
        nutri_group = Group.objects.create(name="Nutricionist")

        user = get_user_model().objects.create_user(username="testuser1", email="testuser1@example.com",
                                                    password="12345")
        nutri = get_user_model().objects.create_user(username="nutri", email="nutri@example.com", password="12345")
        nutri.groups.add(nutri_group)

        plan1 = Plan.objects.create(name="plan1", owner=user, is_public=False)
        plan2 = Plan.objects.create(name="plan2", owner=nutri, is_public=False)
        plan3 = Plan.objects.create(name="plan3", owner=nutri, is_public=True)

        FollowingPlan.objects.create(id_plan=plan3, id_user=user)

        super().login_user("testuser1", "12345")

    def tearDown(self):
        """
        This method is called after each test method runs. It logs out the user.
        :return:
        """
        super().logout_user()
        
    @classmethod
    def tearDownClass(cls):
        """
        This method can be used to perform any clean-up actions that are necessary after running all the test methods in the class.
        :return:
        """

        super().tearDownClass()
        

    def _open_modal(self, xpath_dots, xpath_publish):
        """
        This method opens a modal dialog by finding the elements specified by xpath_dots and xpath_publish, clicking on them, and waiting for 10 seconds.
        :param xpath_dots:
        :param xpath_publish:
        :return:
        """

        dots = self.selenium.find_element(By.XPATH, xpath_dots)
        self.selenium.execute_script("arguments[0].click()", dots)
        self.selenium.implicitly_wait(10)

        publish = self.selenium.find_element(By.XPATH, xpath_publish)
        self.selenium.execute_script("arguments[0].click()", publish)
        self.selenium.implicitly_wait(10)

    def _try_to_public(self, xpath_dots, xpath_publish):
        """
        This method tries to make a plan public by calling _open_modal, finding the public toggle button, clicking it, and then closing the modal.
        :param xpath_dots:
        :param xpath_publish:
        :return:
        """
        self._open_modal(xpath_dots, xpath_publish)

        toggle = self.selenium.find_element(By.XPATH, '//*[@id="public"]')
        self.selenium.execute_script("arguments[0].click()", toggle)
        exit_button = self.selenium.find_element(By.XPATH, '//*[@id="publish-modal-container"]/div/div[1]')
        self.selenium.execute_script("arguments[0].click()", exit_button)
        self.selenium.implicitly_wait(10)

    def _try_to_send(self, xpath_dots, xpath_publish, user_to):
        """
        This method tries to send a plan to another user by calling _open_modal, filling in the username,
        clicking the submit button, logging out, logging in as the recipient, and checking if the plan was sent successfully.
        :param xpath_dots:
        :param xpath_publish:
        :param user_to:
        :return:
        """
        self._open_modal(xpath_dots, xpath_publish)

        input = self.selenium.find_element(By.XPATH, '//*[@id="sending-username"]')

        input.send_keys(user_to)

        submit = self.selenium.find_element(By.XPATH, '//*[@id="send-plan-btn"]')
        self.selenium.execute_script("arguments[0].click()", submit)

        super().logout_user()
        super().login_user("nutri", "12345")

        plans = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[2]/div')

        self.assertTrue("plan1" in plans.text)

    def _uknown_user(self, xpath_dots, xpath_publish, user_to):
        """
        This method tries to send a plan to a non-existent user, expecting an error.
        It calls _open_modal, fills in the username, clicks the submit button, and checks for an error message in the popup.
        :param xpath_dots:
        :param xpath_publish:
        :param user_to:
        :return:
        """
        self._open_modal(xpath_dots, xpath_publish)

        input = self.selenium.find_element(By.XPATH, '//*[@id="sending-username"]')

        input.send_keys(user_to)

        submit = self.selenium.find_element(By.XPATH, '//*[@id="send-plan-btn"]')
        self.selenium.execute_script("arguments[0].click()", submit)

        pop_up = self.selenium.find_element(By.XPATH, '//*[@id="alert"]')

        self.assertTrue("error-col" in pop_up.get_attribute("class").split())


    def test_public_plan_non_nutri(self):
        """
        This test checks that a non-nutritionist user cannot make a plan public. It calls _try_to_public and verifies that an error message is shown.
        :return:
        """

        self._try_to_public(
            xpath_dots='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/i',
            xpath_publish='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/span'
        )

        pop_up = self.selenium.find_element(By.XPATH, '//*[@id="alert"]')

        self.assertTrue("show" in pop_up.get_attribute("class").split())

    def test_public_nutri(self):
        """
        This test checks that a nutritionist user can make a plan public.
        It logs in as nutri, calls _try_to_public, and verifies that the public status element is present.
        :return:
        """

        super().logout_user()
        super().login_user("nutri", "12345")

        self._try_to_public(
            xpath_dots='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/i',
            xpath_publish='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/span'
        )

        try:
            self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[1]/span/span[2]')
        except NoSuchElementException:
            self.assertTrue(False)

    def test_send_plan(self):
        """
        This test checks that a plan can be sent to another user. It calls _try_to_send with user_to="nutri".
        :return:
        """
        self._try_to_send(
            xpath_dots='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/i',
            xpath_publish='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/span',
            user_to="nutri"
        )

    def test_send_plan_uknown_user(self):
        """
        This test checks that an error occurs when trying to send a plan to a non-existent user. It calls _uknown_user with user_to="nutri2".
        :return:
        """
        self._uknown_user(
            xpath_dots='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/i',
            xpath_publish='/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/span',
            user_to="nutri2"
        )







