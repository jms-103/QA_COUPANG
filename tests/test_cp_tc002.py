from urllib import parse
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from pages.main_page import MainPage
from pages.product_list_page import ProductListPage
from common.common import Common
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# 쿠팡 - 장바구니 담기 기능 테스트

@pytest.mark.usefixtures('driver')
class TestCpTC002:
    def test_cart(self, driver):
        wait = WebDriverWait(driver, 10)
        common = Common(driver)
        main_page = MainPage(driver)
        product_list_page = ProductListPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        KEY_WORD = '아이패드'

        try:
            # 메인페이지 시작
            main_page.move_main()
            common.sleep_random()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, common.get_search())
                )
            )
            common.sleep_random()

            # 키워드 검색
            common.search_items(KEY_WORD)

            # 검색결과 대기
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            # 첫 상품 클릭
            common.sleep_random()
            product_list_page.click_topN_product(0)

            # 상품 정보 대기
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, product_page.get_first_check_option())
                )
            )
            # 장바구니 담기
            product_page.click_cart()

            # 메인 페이지로 이동해도
            # 옵션 변경 유지 되는지 확인
            main_page.move_main()

            # 장바구니 페이지로 이동
            cart_page.move_cart()

            # 수량 추가도 해보고
            common.sleep_random()
            cart_page.click_quantity_plus()
            common.sleep_random()
            cart_page.click_quantity_plus()
            common.sleep_random()

            # 수량 감소도 해보고
            common.sleep_random()
            cart_page.click_quantity_minus()
            common.sleep_random()
            cart_page.click_quantity_minus()
            common.sleep_random()

            # 수량 직접 입력도 해보고 
            cart_page.input_quantity(55)
            common.sleep_random()
            # 수량 변경에 따른 가격 비교도 해야 함.





        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False