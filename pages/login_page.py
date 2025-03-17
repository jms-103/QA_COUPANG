import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from common.common import Common


class LoginPage(Common):
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def get_email(self) -> str:
        return f'//input[@name="email"]'
    
    def get_password(self) -> str:
        return f'//input[@name="password"]'
    
    def get_login_button(self) -> str:
        return f"//button[contains(@class, 'login__button--submit') and contains(text(), '로그인')]"
    
    def login(self, em: str, pw: str) -> None:
        email = self.driver.find_element(By.XPATH, self.get_email())
        password = self.driver.find_element(By.XPATH, self.get_password())
        login_button = self.driver.find_element(By.XPATH, self.get_login_button())

        email.send_keys(em)
        self.sleep_random()
        password.send_keys(pw)
        self.sleep_random()

        login_button.click()
