from random import randrange
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
from pages.header_view import HeaderView
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.product_list_page import ProductListPage

# 쿠팡 - 상품 옵션 변경 및 반영 테스트

@pytest.mark.usefixtures('driver')
class TestCpTC003:
    def test_options(self, driver):
        time_sleep_random = (randrange(3, 20)) * 0.1
        wait = WebDriverWait(driver, 10)
        cart_page = CartPage(driver)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        product_list_page = ProductListPage(driver)
        product_page = ProductPage(driver)
        
        KEY_WORD = '아이패드'

        try:
            compare_a = ''
            compare_b = ''

            # 메인페이지 시작
            main_page.move_main()
            header_view.sleep_random()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_search())
                )
            )
            header_view.sleep_random()

            # 키워드 검색
            header_view.search_items(KEY_WORD)

            # 검색결과 대기
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )

            # 첫 상품 클릭
            header_view.sleep_random()
            product_list_page.click_topN_product(0)

            # 상품 정보 대기
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, product_page.get_first_check_option())
                )
            )

            # 옵션 선택
            compare_a = product_page.click_every_first_options()

            # 장바구니 담기
            product_page.click_cart()

            # 메인 페이지로 이동해도
            # 옵션 변경 유지 되는지 확인
            main_page.move_main()

            # 장바구니 페이지로 이동
            cart_page.move_cart()

            compare_b = cart_page.product_name_str()

            assert compare_a == compare_b

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False