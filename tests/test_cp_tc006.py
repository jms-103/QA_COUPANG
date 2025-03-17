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
from pages.login_page import LoginPage
import os
from dotenv import load_dotenv


# 쿠팡 - 최근 본 상품 목록 테스트 케이스

@pytest.mark.usefixtures('driver')
class TestCpTC006:

    # 상위 3개 특가 물품 검증
    @pytest.mark.parametrize('PRODUCT_NUM', [0, 1, 2])
    def test_special_price(self, driver, PRODUCT_NUM):
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        login_page = LoginPage(driver)

        load_dotenv(verbose=True)
        COUPANG_EMAIL = os.getenv('EMAIL')
        COUPANG_PASSWORD = os.getenv('PASSWORD')

        count_a = 0
        count_b = 0

        try:
            # 메인 페이지로 이동
            main_page.move_main()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_login())
                )
            )
            header_view.click_login()

            # 로그인 페이지 진입
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, login_page.get_email())
                )
            )

            # 로그인
            login_page.login(COUPANG_EMAIL, COUPANG_PASSWORD)
            header_view.sleep_random()
            
            # 검색창 뜰 때 까지
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_search())
                )
            )
            header_view.sleep_random()
            main_page.scroll_down()
            header_view.sleep_random()

            count_a = main_page.get_count_recently_viewed()


            # 최근 조회한 항목이 있어서 삭제가 가능하다면 삭제
            if main_page.get_delete_recently_viewed(0):
                main_page.click_delete_recently_viewed(0)
                count_b = main_page.get_count_recently_viewed()

                assert count_a == count_b    
            
            

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False