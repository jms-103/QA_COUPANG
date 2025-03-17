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

@pytest.mark.usefixtures('driver')
class TestMainPage:
    @pytest.mark.skip()
    def test_open_main_page(self, driver):
        header_view = HeaderView(driver)

        ITEMS_XPATH = "//form//ul/li"
        ITEM_NAME = parse.quote('노트북')

        try:
            main_page = MainPage(driver)
            main_page.move_main()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

            header_view.sleep_random()
            main_page.click_LINK_TEXT('로그인')
            assert "login" in driver.current_url

        except NoSuchElementException as e:
            assert False


    @pytest.mark.skip()
    def test_click_link_text(self, driver:WebDriver):
        try:
            main_page = MainPage(driver)
            main_page.move_main()

            header_view.sleep_random()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url
            header_view.sleep_random()

            main_page.click_LINK_TEXT('로그인')
            assert "login" in driver.current_url
            driver.save_screenshot('메인페이지-로그인-성공.png')

            header_view.sleep_random()
            driver.back()

            # 비로그인 테스트이므로 마이쿠팡을 클릭시 로그인해야 함.
            main_page.click_LINK_TEXT('마이쿠팡')
            # assert "login" in driver.current_url
            driver.save_screenshot('메인페이지-로그인-성공.png')

            header_view.sleep_random()
            driver.back()

            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url

            header_view.sleep_random()

            main_page.click_LINK_TEXT('회원가입')
            assert "memberJoinFrm" in driver.current_url
            driver.save_screenshot('메인페이지-회원가입입-성공.png')
        except NoSuchElementException as e:
            assert False
        except TimeoutException as e:
            driver.save_screenshot('메인페이지-검색-실패-타임아웃.png')
            assert False


    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_search_items(self, driver):
        ITEMS_XPATH = "//form//ul/li"
        ITEM_NAME = parse.quote('노트북')
        try:
            main_page = MainPage(driver)
            main_page.move_main()

            header_view.sleep_random()

            main_page.search_items('노트북')
            assert "/search" in driver.current_url

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ITEMS_XPATH))
            )

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            assert len(items) > 0
            assert ITEM_NAME in driver.current_url
            driver.save_screenshot('메인페이지-검색-성공.png')


        except NoSuchElementException as e:
            driver.save_screenshot('메인페이지-검색-실패-노서치.png')
            assert False
        
        except TimeoutException as e:
            driver.save_screenshot('메인페이지-검색-실패-타임아웃.png')
            assert False