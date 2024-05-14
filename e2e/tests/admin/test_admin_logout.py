from selenium.webdriver.common.by import By

from e2e.tests.base_selenium_test import BaseSeleniumTest


class TestLogout(BaseSeleniumTest):
    def test_admin_logout_success(self):
        # Logging in
        driver = self.driver
        url = self.live_server_url + "/admin/"
        driver.get(url)
        username = self.super_user.username
        password = self.user_password
        self.login(driver, username, password)

        # Logging out
        driver.find_element(By.XPATH, "//*[@id='logout-form']/button").click()
        self.assertEqual(
            driver.current_url,
            self.live_server_url + "/admin/logout/",
            "logout success",
        )
