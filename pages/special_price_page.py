import re
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.header_view import HeaderView

class SpecialPricePage(HeaderView):
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def move_special_price(self):
        return self.driver.get(self.get_special_price_url())

    def get_original_price(self, index) -> str:
        return f'(//span[contains(@class, "original_price")])[{index+1}]'

    def get_sale_price(self, index) -> str:
        return f'(//span[contains(@class, "sale_price")])[{index+1}]'

    def get_discount_rate(self, index) -> str:
        return f'(//span[contains(@class, "discount_rate")])[{index+1}]'
    
    def get_filter_discount(self, index) -> str:
        return f'(//div[@id="searchPriceFilter"])[1]/ul/li[{index+1}]/a'
    
    def click_filter_discount_rate(self, rate_index: int) -> int:
        if rate_index not in [1, 2, 3, 4]:  # [10% 이상, 25% 이상, 50% 이상, 70% 이상]
            rate_index = 1  # 범위 안에 없는 인덱스를 골라서 잘못될거면 10% 이상을 고르도록 방어코드
        rate_element = self.driver.find_element(By.XPATH, self.get_filter_discount(rate_index))
        rate_element.click()
        return int((rate_element.text)[:2])


    # 원가, 할인율, 할인가 비교
    def is_correct_discount(self, index) -> bool:
        original_price_text = self.driver.find_element(By.XPATH, self.get_original_price(index)).text
        original_price = int(re.sub(r'[^0-9]', '', original_price_text))  # 숫자만 추출

        sale_price_text = self.driver.find_element(By.XPATH, self.get_sale_price(index)).text
        sale_price = int(re.sub(r'[^0-9]', '', sale_price_text))  # 숫자만 추출

        discount_rate_text = self.driver.find_element(By.XPATH, self.get_discount_rate(index)).text
        discount_rate = int(re.sub(r'[^0-9]', '', discount_rate_text))  # 숫자만 추출

        a = int(round(original_price * ((100 - discount_rate)*0.01), -3))  # 100의 자리에서 반올림
        b = int(round(sale_price, -3))  # 100의 자리에서 반올림
        return a == b
