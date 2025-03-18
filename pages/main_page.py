import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver

from common.common import Common

class MainPage(Common):

    def __init__(self, driver:WebDriver):
        self.driver = driver

    # 최근 본 상품 삭제
    def get_delete_recently_viewed(self, index) -> str:
        return f"(//ul[@class='recently-viewed-page']/li[@class='recently-viewed-item'])[{index+1}]/a[@href='삭제']"
    
    def get_count_recently_viewed(self) -> int:
        return int(self.driver.find_element(By.XPATH, f'//div[@class="recently-viewed-products"]/em[@class="total-element"]').text)
        
    
    # 최근 본 상품 조회를 위해 스크롤 내림
    def scroll_down_recently_viewed(self) -> None:
        self.driver.execute_script("""
        const element = document.querySelector('.recently-viewed-products');
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        """
        )

    def click_delete_recently_viewed(self, index) -> str:
        element_to_hover = self.driver.find_element(By.XPATH, self.get_delete_recently_viewed(index))
        self.mouse_move_click_action(element_to_hover)
        
    def refresh(self) -> None:  # 최근 본 상품 삭제 이후를 보기 위함
        self.driver.execute_script('location.reload()')
        
    # 메인 페이지 열기
    def move_main(self) -> None:
        self.driver.get(self.get_main_url())
        
        

    def click_LINK_TEXT(self, link_text: str) -> None:
        login_button = self.driver.find_element(By.LINK_TEXT, link_text)
        login_button.click()

# https://login.coupang.com/login/memberJoinFrm.pang