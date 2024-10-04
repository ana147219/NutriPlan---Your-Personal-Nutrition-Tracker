'''
Tijana Gasic 0247/2021
'''


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

class SeleniumTest(StaticLiveServerTestCase):

    """
    class is testing basic login/out functionalities
    """



    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def login_user(cls, username, password):
        """
        tests basic login functionality
        :param username:
        :param password:
        :return: logged user
        """

        cls.selenium.get(f"{cls.live_server_url}/login")
        cls.selenium.implicitly_wait(10)

        input_username = cls.selenium.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/form/div[1]/input")
        input_password = cls.selenium.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/form/div[2]/input")

        input_username.send_keys(username)
        input_password.send_keys(password)


        cls.selenium.find_element(By.XPATH, '//*[@id="login_btn"]').click()

    @classmethod
    def logout_user(cls):
        """
        tests logout functionality
        :return:
        """
        logout_button = cls.selenium.find_element(By.XPATH, '//*[@id="logout-btn"]')
        cls.selenium.execute_script("arguments[0].click()", logout_button)



