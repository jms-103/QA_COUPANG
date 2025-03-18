import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from common.common import Common
from selenium.webdriver.common.action_chains import ActionChains

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
        actions = ActionChains(self.driver)
        email = self.driver.find_element(By.XPATH, self.get_email())
        password = self.driver.find_element(By.XPATH, self.get_password())
        # login_button = self.driver.find_element(By.XPATH, self.get_login_button())

        # 각 글자를 한 글자씩 입력합니다.
        # for char in em:
            # Use JavaScript to simulate keypress events
            # self.sleep_random()
            # self.driver.execute_script("arguments[0].value += arguments[1];", email, char)
        # email.send_keys(em)
        # password.send_keys(pw)

        # 각 글자를 한 글자씩 입력합니다.
        # for char in em:
            # Use JavaScript to simulate keypress events
            # self.sleep_random()
            # self.driver.execute_script("arguments[0].value += arguments[1];", password, char)
        actions.move_to_element(email).click().pause(0.1)
        for char in em:
            actions.send_keys(char).pause(4)
        actions.perform()


        self.sleep_random()
        actions.move_to_element(password).click().pause(0.1)
        for char in pw:
            actions.send_keys(char).pause(4)
        actions.perform()
        self.sleep_random()

        self.enter_login()
        # self.mouse_move_click_action(login_button)

