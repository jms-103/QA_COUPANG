from urllib import parse
import re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from pages.main_page import MainPage
from pages.cart_page import CartPage
from common.common import Common
from pages.product_list_page import ProductListPage
from pages.product_page import ProductPage
from pages.special_price_page import SpecialPricePage
from random import randrange

# 쿠팡 - 판매자 특가 페이지 테스트케이스

@pytest.mark.usefixtures('driver')
class TestCpTC005:

    # 상위 3개 특가 물품 검증
    @pytest.mark.parametrize('PRODUCT_NUM', [0, 1, 2])
    def test_special_price(self, driver, PRODUCT_NUM):
        wait = WebDriverWait(driver, 10)
        special_price_page = SpecialPricePage(driver)

        try:
            # 메인 페이지로 이동
            special_price_page.move_special_price()
            # 물건(가격) 하나 뜰 때 까지
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, special_price_page.get_original_price())
                )
            )
            
            assert special_price_page.is_correct_discount(PRODUCT_NUM)

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False


    # 할인율 필터 검증
    @pytest.mark.parametrize('FILTER_INDEX', [1, 2, 3, 4])
    @pytest.mark.parametrize('PRODUCT_NUM', [0, 1, 2])
    def test_filter_discount_rate(self, driver, FILTER_INDEX, PRODUCT_NUM):
        wait = WebDriverWait(driver, 10)
        special_price_page = SpecialPricePage(driver)
        common = Common(driver)

        try:
            product_rate = 0
            filter_rate = 0

            # 메인 페이지로 이동
            special_price_page.move_special_price()
            # 물건(가격) 하나 뜰 때 까지
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, special_price_page.get_original_price())
                )
            )
            common.sleep_random()
            filter_rate = special_price_page.click_filter_discount_rate(FILTER_INDEX)
            # 물건(가격) 하나 뜰 때 까지
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, special_price_page.get_original_price())
                )
            )
            common.sleep_random()
            discount_rate_text = driver.find_element(By.XPATH, special_price_page.get_discount_rate(PRODUCT_NUM)).text
            product_rate = int(re.sub(r'[^0-9]', '', discount_rate_text))  # 숫자만 추출
            
            assert filter_rate <= product_rate


        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False
