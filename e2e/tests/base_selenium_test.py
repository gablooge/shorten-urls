import os

from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from e2e.tests.utils import helpers


@tag("e2e")
class BaseSeleniumTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        ContentType.objects.clear_cache()
        super().setUpClass()
        options = Options()
        options.add_argument("--disable-dev-shm-usage")
        # overcome limited resource problems
        options.add_argument("--no-sandbox")
        # Bypass OS security model
        if os.environ.get("HEADLESS"):
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        if not os.environ.get("HEADLESS"):
            driver.set_window_size(1000, 1080)
        cls.driver = driver
        cls.port = 8888

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def login(self, driver, username, password):
        url = self.live_server_url + "/admin/login/"
        driver.get(url)
        username_elem = driver.find_element(By.NAME, "username")
        username_elem.clear()
        username_elem.send_keys(username)

        password_elem = driver.find_element(By.NAME, "password")
        password_elem.clear()
        password_elem.send_keys(password)
        driver.find_element(By.XPATH, "//*[@id='login-form']/div[3]/input").click()

        return driver

    def setUp(self):
        self.super_user = helpers.createSuperUser()
        self.user_password = "sangatrahasia"
