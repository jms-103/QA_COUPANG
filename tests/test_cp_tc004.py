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

# 쿠팡 - 검색 필터 기능 테스트

@pytest.mark.parametrize('COST', [([500000, 1000000]), ([200000, 2000000])])
@pytest.mark.usefixtures('driver')
class TestCpTC004:

    # 가격 범위 필터 테스트
    def test_price_filter(self, driver, COST):
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        product_list_page = ProductListPage(driver)
        
        KEYWORD = '노트북'

        try:
            result = []

            # 메인 페이지로 이동
            main_page.move_main()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_search())
                )
            )
            header_view.sleep_random()

            # 키워드 검색
            header_view.search_items(KEYWORD)

            # 상품리스트 페이지
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            # 가격 필터링
            product_list_page.filter_price_range(COST[0], COST[1])
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            result = product_list_page.get_top3_price_list()

            # 최솟값 최댓값 필터링 여부 확인
            for r in result:
                assert COST[0] <= r <= COST[1]

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False


    # 브랜드 필터 테스트
    @pytest.mark.parametrize("FILTER_KEYWORD", ['삼성', 'LG'])
    def test_brand_filter(self, driver, FILTER_KEYWORD):
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        product_list_page = ProductListPage(driver)
        

        KEYWORD = '노트북'

        try:
            result = {}

            # 메인 페이지로 이동
            main_page.move_main()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_search())
                )
            )
            header_view.sleep_random()

            # 키워드 검색
            header_view.search_items(KEYWORD)

            # 상품리스트 페이지
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            # 브랜드 필터링
            product_list_page.click_brand_filter(FILTER_KEYWORD)
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            result = product_list_page.get_top3_product_dict()

            # 상품 목록들 중 상품명에 브랜드 이름이 포함돼 있는지 확인
            assert FILTER_KEYWORD in result.values()


        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False


    # 별점 필터 테스트
    @pytest.mark.parametrize('RATING', [4, 3, 2, 1])
    def test_rating_filter(self, driver, RATING):
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        product_list_page = ProductListPage(driver)
        

        KEYWORD = '노트북'

        try:
            result = {}

            # 메인 페이지로 이동
            main_page.move_main()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_search())
                )
            )
            header_view.sleep_random()

            # 키워드 검색
            header_view.search_items(KEYWORD)

            # 상품리스트 페이지
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            # 별점 필터링
            product_list_page.click_rating_filter(RATING)  
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            result = product_list_page.get_top3_rating_list()

            for r in result:
                # 별점보다 높은 결과가 떴는지 확인
                assert RATING <= r  

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False


    # 종합 필터 테스트
    @pytest.mark.parametrize('RATING', [4, 3, 2, 1])
    @pytest.mark.parametrize("FILTER_KEYWORD", ['삼성', 'LG'])
    @pytest.mark.parametrize('COST', [([500000, 1000000]), ([200000, 2000000])])
    def test_multiple_filter(self, driver, RATING, FILTER_KEYWORD, COST):
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        product_list_page = ProductListPage(driver)
        

        KEYWORD = '노트북'
        tag_count = 0

        rating_assert_string = str(RATING)+'점 이상'
        cost_assert_string = str(COST[0])+'원~'+str(COST[1])+'원'

        try:
            result = {}

            # 메인 페이지로 이동
            main_page.move_main()
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, header_view.get_search())
                )
            )
            header_view.sleep_random()

            # 키워드 검색
            header_view.search_items(KEYWORD)

            # 상품리스트 페이지
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            header_view.sleep_random()

            # 1. 가격 필터링
            product_list_page.filter_price_range(COST[0], COST[1])
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            tag_count += 1
            header_view.sleep_random()

            # 2. 브랜드 필터링
            product_list_page.click_brand_filter(FILTER_KEYWORD)
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            tag_count += 1
            header_view.sleep_random()

            # 3. 별점 필터링
            product_list_page.click_rating_filter(RATING)  
            wait.until(
                EC.presence_of_element_located(
                    # 첫 상품 나오는지
                    (By.XPATH, product_list_page.get_product_name_topN(0))
                )
            )
            tag_count += 1
            header_view.sleep_random()
        
            result = product_list_page.get_tags_list(tag_count)

            # 선택한 필터 목록에 뜨는지 검증
            # 선택한 필터: 삼성전자, 4점이상, 200000원~2000000원
            for r in result:
                if r[1:] == '점 이상':  # ex) '4'+'점 이상'
                    assert r == rating_assert_string
                elif '원~' in r:  # ex) '원~' in 200000원~2000000원
                    assert r == cost_assert_string
                else:  
                    assert FILTER_KEYWORD in r  # ex) '삼성' in '삼성전자
                

        except NoSuchElementException as e:
            driver.save_screenshot('요소 없음.png')
            assert False

    # 필터 리셋 테스트
    @pytest.mark.parametrize('RATING', [4, 3, 2, 1])
    def test_reset(self, driver, RATING):
        wait = WebDriverWait(driver, 10)
        main_page = MainPage(driver)
        header_view = HeaderView(driver)
        product_list_page = ProductListPage(driver)
        

        KEYWORD = '노트북'

        tag_count = 0

        
        result = {}

        # 메인 페이지로 이동
        main_page.move_main()
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, header_view.get_search())
            )
        )
        header_view.sleep_random()

        # 키워드 검색
        header_view.search_items(KEYWORD)

        # 상품리스트 페이지
        wait.until(
            EC.presence_of_element_located(
                # 첫 상품 나오는지
                (By.XPATH, product_list_page.get_product_name_topN(0))
            )
        )
        header_view.sleep_random()

        # 별점 필터링
        product_list_page.click_rating_filter(RATING)  
        wait.until(
            EC.presence_of_element_located(
                # 첫 상품 나오는지
                (By.XPATH, product_list_page.get_product_name_topN(0))
            )
        )
        tag_count += 1
        header_view.sleep_random()

        assert product_list_page.get_tags_list(tag_count)

        wait.until(
            EC.presence_of_element_located(
                # 리셋 버튼 나오는지
                (By.XPATH, product_list_page.get_reset_filter())
            )
        )

        # 필터 리셋 클릭.
        product_list_page.click_reset_filter()
        header_view.sleep_random()

        try:
            product_list_page.get_tags_list(tag_count)

        except NoSuchElementException as e:
            # 필터가 초기화 됐으므로
            # "선택한 필터:" 요소가 없어야 함.
            assert True