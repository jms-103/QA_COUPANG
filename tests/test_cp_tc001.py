import pickle
import sys
import os
import time
import pytest
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from common.common import Common
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.product_list_page import ProductListPage


''''
쿠팡 - 상품 검색 기능 테스트

웹 크롬으로 접속 후 검색 기능 정상 작동 여부 확인
'''


@pytest.mark.usefixtures('driver')
class TestCpTC001:

    def test_search(self, driver):
        
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        common = Common(driver)
        login_page = LoginPage(driver)
        product_list_page = ProductListPage(driver)

        load_dotenv(verbose=True)
        COUPANG_EMAIL = os.getenv('EMAIL')
        COUPANG_PASSWORD = os.getenv('PASSWORD')
        
        SUB_KEYWORD = ['아이패드', '아이폰 16 케이스', '아이패드 에어']
        KEY_WORD = '노트북'

        compare_a = {}
        compare_b = {}

        # 로그인 -> compare_a
        try:
            main_page.move_main()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, common.get_login())
                )
            )

            # 로그인 페이지 진입
            login_page.click_login()

            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, login_page.get_email())
                )
            )

            common.sleep_random()
            login_page.login(COUPANG_EMAIL, COUPANG_PASSWORD)
            common.sleep_random()

            # time.sleep(120)
            # pickle.dump(driver.get_cookies(), open("coupang_cookies.pkl", "wb"))  # 최초 로그인 후 쿠키 저장시에만
            

            # 메인페이지
            # 검색
            common.search_item_subkeyword_mimicking(SUB_KEYWORD)
            common.search_items(KEY_WORD)

            # 상품리스트 페이지
            common.sleep_random()
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            # top3 상품명 결과
            compare_a = product_list_page.get_top3_product_dict()
            
        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False

        # 로그아웃 후 -> compare_b
        try:
            common.sleep_random()
            # main_page.move_main()
            common.sleep_random()
            main_page.click_logout()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, common.get_search())
                )
            )
            common.sleep_random()
            # 검색
            common.search_item_subkeyword_mimicking(SUB_KEYWORD)  # 사람흉내용 서브키워드 검색
            common.search_items(KEY_WORD)

            # 상품리스트 페이지
            common.sleep_random()
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            # top3 상품명 결과
            compare_b = product_list_page.get_top3_product_dict()

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False

        
            
        assert compare_a['first'] == compare_b['first']
