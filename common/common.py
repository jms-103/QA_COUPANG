from random import randrange
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Common():
    MAIN_URL = "https://www.coupang.com/"
    CART_URL = "https://cart.coupang.com/cartView.pang"
    SPECIAL_PRICE_URL = "https://www.coupang.com/np/omp"

    time_sleep_random = (randrange(27, 52)) * 0.1

    def scroll_down(self) -> None:
        self.driver.execute_script(
            '''
            window.scrollBy(0, 100)
            '''
        )
    

    def __init__(self, driver:WebDriver):
        self.driver = driver

    def sleep_random(self) -> None:
        time.sleep(self.time_sleep_random)

    def get_main_url(self) -> str:
        return self.MAIN_URL
    
    def get_cart_url(self) -> str:
        return self.CART_URL
    
    def get_special_price_url(self) -> str:
        return self.SPECIAL_PRICE_URL

    def get_search(self) -> str:
        return f'//*[@id="headerSearchKeyword"]'
    
    def get_search_button(self) -> str:
        return f'//*[@id="headerSearchBtn"]'
    
    def get_login(self) -> str:
        return f'//li[@id="login"]/a[@class="login"]'
    
    def get_logout(self) -> str:
        return f'//li[@id="logout"]/a[@class="logout"]'
    
    def click_login(self) -> None:
        self.driver.find_element(By.XPATH, self.get_login()).click()

    def enter_login(self) -> None:
        self.driver.find_element(By.XPATH, self.get_login()).send_keys(Keys.Enter)

    def click_logout(self) -> None:
        self.mouse_move_click_action(
            self.driver.find_element(By.XPATH, self.get_logout())
        )
    
    def search_items(self, item_name:str) -> None:
        actions = ActionChains(self.driver)

        self.sleep_random()
        search_input_box = self.driver.find_element(By.XPATH, self.get_search())
        actions.move_to_element(search_input_box).click().pause(0.1)
        # search_input_box.send_keys(item_name)

        # 각 글자를 한 글자씩 입력합니다.
        # for char in item_name:
            # Use JavaScript to simulate keypress events
        self.sleep_random()
            # self.driver.execute_script("arguments[0].value += arguments[1];", search_input_box, char)
        for char in item_name:
            actions.send_keys(char).pause(4)
        actions.perform()

        self.sleep_random()
        search_button = self.driver.find_element(By.XPATH, self.get_search_button())
        # self.dirver.get()
        # self.mouse_move_click_action(search_button)
        actions.move_to_element(search_input_box).click().pause(0.1)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def search_item_subkeyword_mimicking(self, subkeyword: list) -> None:
        for sk in subkeyword:
            self.search_items(sk)
            self.scroll_down()

    def mouse_move_click_action(self, element) -> None:
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.sleep_random()
        element.click()