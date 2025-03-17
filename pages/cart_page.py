from selenium.webdriver.chrome.webdriver import WebDriver
from common.common import Common
from selenium.webdriver.common.by import By


class CartPage(Common):
    def __init__(self, driver:WebDriver):
        self.driver = driver
        
    def get_title(self) -> str:
        return f'//span[contains(@class, "product-name")]'

    def get_quantity_plus(self) -> str:
        return f'//div[contains(@class, "quantity-input-icon plus")]'

    def get_quantity_minus(self) -> str:
        return f'//div[contains(@class, "quantity-input-icon minus")]'
        
    def get_product_delete(self) -> str:
        return f'//a[@class="delete-option"]'
    
    def get_quantity_input(self) -> str:
        return f'//input[@class="quantity-input"]'
    
    def input_quantity(self, quantity) -> None:
        self.driver.find_element(By.XPATH, self.get_quantity_input).send_keys(quantity)
        
    def click_quantity_plus(self) -> None:
        self.get_quantity_plus().click()

    def click_quantity_minus(self) -> None:
        self.get_quantity_minus().click()
        
    def click_product_delete(self) -> None:
        self.get_product_delete().click()
	  
    # 장바구니 페이지로 이동
    def move_cart(self) -> None:
        self.driver.get(self.get_cart_url())

    def product_name_str(self) -> str:
        return self.driver.find_element(By.XPATH, self.get_title()).text