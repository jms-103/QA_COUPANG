import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from common.common import Common


class ProductPage(Common):
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def get_product_name(self) -> str:
        return f'//div[@class="prod-buy-header"]/h1[@class="prod-buy-header__title"]'

    # 드랍다운 클릭 후 속성선택
    # 색상
    def get_first_dropdown_option_color(self) ->str:
        return f'(//li[@class="prod-option-dropdown-item  "])[position()=1]'

    # 드랍다운 클릭 후 속성선택
    # 저장용량 x 태블릿 연결성
    def get_first_dropdown_option_memory_wifi(self) ->str:  
        return f'(//li[@class="prod-option-dropdown-item"])[position()=1]'

    # 색상을 선택하기 위해 
    # 드랍다운 선택
    def get_dropdown_color(self) ->str:
        return f'(//div[@class="prod-option__item"])[position()=1]'
    
    # 저장용량 x 태블릿 연결성 선택하기 위해 
    # 드랍다운 선택
    def get_dropdown_memory_wifi(self) ->str:
        return f'(//div[@class="prod-option__item"])[position()=2]'
    
    # 내일 도착
    def get_first_radio_option(self) ->str:
        return f'(//span[@class="delivery-type-radio-btn"])[position()=1]'

    # AppleCare+
    def get_first_check_option(self) ->str:
        return f'(//input[@type="checkbox"])[position()=1]'
    
    # 장바구니 담기
    def get_cart(self) ->str:
        return f'//button[@class="prod-cart-btn"]'
    
    def click_dropdown_option_color(self) -> str:
        self.sleep_random()
        self.driver.find_element(By.XPATH, self.get_dropdown_color).click()
        self.sleep_random()
        option = self.driver.find_element(By.XPATH, self.get_first_dropdown_option_color)
        option.click()
        return option.text

    
    def click_dropdown_option_memory_wifi(self) -> str:
        self.sleep_random()
        self.driver.find_element(By.XPATH, self.get_dropdown_memory_wifi).click()
        self.sleep_random()
        option = self.driver.find_element(By.XPATH, self.get_first_dropdown_option_memory_wifi)
        option.click()
        return option.text
    
    def click_every_first_options(self) -> str:
        result = ''
        result += self.driver.find_element(By.XPATH, self.get_product_name()).text
        result += ', '
        # 내일 도착 클릭
        self.sleep_random()
        self.driver.find_element(By.XPATH, self.get_first_radio_option).click
        # AppleCare+ 클릭
        self.sleep_random()
        self.driver.find_element(By.XPATH, self.get_first_radio_option).click
        # 색상 클릭
        self.sleep_random()
        result += self.click_dropdown_option_color()
        result += ', '
        # 저장용량 x 태블릿 연결성 클릭
        self.sleep_random()
        result += self.click_dropdown_option_memory_wifi()
        return result

    def click_cart(self) -> None:
        self.sleep_random()
        self.driver.find_element(By.XPATH, self.get_cart).click()
        


