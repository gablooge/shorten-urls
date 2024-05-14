from selenium.webdriver.common.by import By

from e2e.tests.base_selenium_test import BaseSeleniumTest


class TestLogin(BaseSeleniumTest):
    def test_admin_login_fail(self):
        driver = self.driver
        url = self.live_server_url + "/admin/login/"
        driver.get(url)
        username = self.super_user.username
        password = "wrongpassword"
        self.login(driver, username, password)
        self.assertNotEqual(
            driver.current_url, self.live_server_url + "/admin/", "login success"
        )
        message = driver.find_element(By.XPATH, "//*[@id='content']/p").text
        self.assertEqual(
            message,
            "Please enter the correct username and password for a staff account. "
            "Note that both fields may be case-sensitive.",
        )

    def test_admin_login_success(self):
        driver = self.driver
        url = self.live_server_url + "/admin/login/"
        driver.get(url)
        username = self.super_user.username
        password = self.user_password
        self.login(driver, username, password)
        self.assertEqual(
            driver.current_url, self.live_server_url + "/admin/", "login success"
        )
