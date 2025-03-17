from random import randrange
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class HeaderView():
    MAIN_URL = "https://www.coupang.com/"
    CART_URL = "https://cart.coupang.com/cartView.pang"
    SPECIAL_PRICE_URL = "https://www.coupang.com/np/omp"


    time_sleep_random = (randrange(3, 20)) * 0.1
    

    def __init__(self, driver:WebDriver):
        self.driver = driver

    def sleep_random(self) -> None:
        self.time_sleep_random
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

    def click_logout(self) -> None:
        self.driver.find_element(By.XPATH, self.get_logout()).click()
    
    def search_items(self, item_name:str) -> None:
        time_sleep_random = (randrange(3, 20)) * 0.1

        search_input_box = self.driver.find_element(By.XPATH, self.get_search())
        search_input_box.send_keys(item_name)
        self.sleep_random
        search_button = self.driver.find_element(By.XPATH, self.get_search_button())
        search_button.click()