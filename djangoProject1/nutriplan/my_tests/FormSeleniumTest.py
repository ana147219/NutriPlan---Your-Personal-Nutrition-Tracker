'''
Tijana Gasic 0247/2021
'''

from django.contrib.auth.models import Group
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model

from nutriplan.my_models.Tag import Tag
from nutriplan.my_tests.SeleniumTest import SeleniumTest

class FormSeleniumTest(SeleniumTest):

    """
    test for testing form behaviour using selenium
    """


    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):

        """
        sets the initial state
        :return:
        """
        self.nutri_group = Group.objects.create(name="Nutricionist")

        self.gf_tag = Tag.objects.create(name='gluten free')
        self.vegan_tag = Tag.objects.create(name='vegan')
        self.cd_tag = Tag.objects.create(name='calorie deficit')
        self.kdp_tag = Tag.objects.create(name="keto diet plan")
        self.lcp_tag = Tag.objects.create(name="low calorie plan")
        self.hpp_tag = Tag.objects.create(name="high protein plan")

        self.User = get_user_model()

        self.user1 = self.User.objects.create_user(username='testuser1', email='testuser1@example.com',
                                                   password='12345')
        self.user2 = self.User.objects.create_user(username='testuser2', email='testuser2@example.com',
                                                   password='12345')

        self.nutri = self.User.objects.create_user(username='nutri', email='nutri@example.com', password='12345')
        self.nutri.groups.add(self.nutri_group)

    def tearDown(self):

        super().logout_user()

    def _send_from(self):
        """
        this function is testing if a form is sent in a correct way
        where all the values are fixed as the one user inputed
        :return:
        """

        order_form_button = self.selenium.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/button')
        self.selenium.execute_script("arguments[0].click()", order_form_button)

        height = self.selenium.find_element(By.XPATH, '//*[@id="height"]')
        weight = self.selenium.find_element(By.XPATH, '//*[@id="weight"]')

        height.send_keys(170)
        weight.send_keys(55)

        checkbox_input = self.selenium.find_element(By.XPATH, '//*[@id="vegan"]')
        self.selenium.execute_script("arguments[0].click()", checkbox_input)

        description = self.selenium.find_element(By.XPATH, '//*[@id="description"]')
        description.send_keys("Some text")

        confirm_button = self.selenium.find_element(By.XPATH, '/html/body/div[2]/form/div/div/div/center/button')
        self.selenium.execute_script('arguments[0].click()', confirm_button)

    def _check_form(self):

        """
        this function is testing if a form looks the same  way its
        been when user sent it
        :return:
        """
        noti_button = self.selenium.find_element(By.XPATH, '//*[@id="notifications-div"]/button')
        self.selenium.execute_script("arguments[0].click()", noti_button)

        check_form_btn = self.selenium.find_element(By.CLASS_NAME, 'btn-success')
        self.selenium.execute_script("arguments[0].click()", check_form_btn)

        height = self.selenium.find_element(By.XPATH, '//*[@id="height"]')
        weight = self.selenium.find_element(By.XPATH, '//*[@id="weight"]')
        non_checked = self.selenium.find_element(By.XPATH, '//*[@id="gluten_free"]')
        checked = self.selenium.find_element(By.XPATH, '//*[@id="vegan"]')
        description = self.selenium.find_element(By.XPATH, '//*[@id="description"]')

        self.assertEqual(float(height.get_attribute("value")), 170.0)
        self.assertEqual(float(weight.get_attribute("value")), 55.0)
        self.assertFalse(non_checked.get_attribute("checked"))
        self.assertTrue(checked.get_attribute("checked"))
        self.assertEqual(description.get_attribute("value"), "Some text")

    def test_form_and_check(self):

        """
        this function is testing if a form is checked for the correct user
        :return:
        """

        self.login_user("testuser1", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_nutri?nutri_id={self.nutri.id}")

        self._send_from()

        self.logout_user()

        self.login_user('nutri', '12345')

        self._check_form()

    def _dismiss_form(self):
        """
        this function checks if a form is dismissed in the right way
        :return:
        """
        noti_button = self.selenium.find_element(By.XPATH, '//*[@id="notifications-div"]/button')
        self.selenium.execute_script("arguments[0].click()", noti_button)

        dismiss_button = self.selenium.find_element(By.CLASS_NAME, 'noti-dismiss-btn')
        self.selenium.execute_script("arguments[0].click()", dismiss_button)

        self.logout_user()

        self.login_user("testuser1", "12345")

        notifications = self.selenium.find_element(By.XPATH, '//*[@id="notifications-div"]')

        self.assertTrue('Request dismissed' in notifications.text)

    def test_dismissed_form(self):

        """
        this function checks if a form is dismissed in the right way for the correct user
        :return:
        """

        self.login_user("testuser1", "12345")

        self.selenium.get(f"{self.live_server_url}/preview_nutri?nutri_id={self.nutri.id}")

        self._send_from()

        self.logout_user()

        self.login_user('nutri', '12345')

        self._dismiss_form()