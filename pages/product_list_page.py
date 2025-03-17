import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from header_view import HeaderView
import re

class ProductListPage(HeaderView):
    def __init__(self, driver:WebDriver):
        self.driver = driver
        
    def get_product_name_topN(self, n:int) -> str:
        return f"(//ul[@id='productList']/li[@class='search-product  '])[{n+1}]/a/dl/dd/div/div[@class='name']"
    
    def get_price_topN(self, n:int) -> str:
        return f"(//ul[@id='productList']/li[@class='search-product  '])[{n+1}]/a/dl/dd/div/div[@class='price-area ']/div/div/em/strong[@class='price-value']"
    
    def get_rating_topN(self, n:int) -> str:
        return f'(//ul[@id="productList"]/li[@class="search-product  "])[{n}]/a/dl/dd/div/div[@class="other-info"]/div/span/em[@class="rating"]'
        
    def get_price_range_min(self) -> str:
        return f'//input[@class="param-pricerange" and @title="minPrice"]'
    
    def get_price_range_max(self) -> str:
        return f'//input[@class="param-pricerange" and @title="maxPrice"]'
        
    def get_price_range_submit(self) -> str:
        return f'//a[@class="btn-price-submit"]'

    def get_filter_brandname(self, brand) -> str:
        return f'//div[@id="searchBrandFilter"]/ul/li/label[contains(text(), {brand})]'
        
    # 1 ~ 4점 이상 별점
    def get_filter_rating(self, star_over) -> str:
        return f'//div[@id="searchRatingFilter"]/ul/li/label[contains(text(), "{star_over}점 이상")]'

    def get_reset_filter(self) -> str:
        return f"//div[@class='search-filter-reset']"
    
    def get_filter_tag_N(self, n: int) -> str:
        return f'(//div[@class="search-query-result"]/dl[@class="search-selected-filters"]/dd/a)[{n+1}]'
        
    def filter_price_range(self, min_price: int, max_price: int) -> None:
        min_p = self.driver.find_element(By.XPATH, self.get_price_range_min())
        max_p = self.driver.find_element(By.XPATH, self.get_price_range_max())
        min_p.send_keys(min_price)
        self.sleep_random()
        max_p.send_keys(max_price)
        self.sleep_random()
        self.driver.find_element(By.XPATH, self.get_price_range_submit()).click()
        
    def click_reset_filter(self) -> None:
        self.driver.find_element(By.XPATH, self.get_reset_filter()).click()
        
    def get_top3_product_dict(self) -> dict:
        result = {}
        first = self.driver.find_element(By.XPATH, self.get_product_name_topN(0)).text
        second = self.driver.find_element(By.XPATH, self.get_product_name_topN(1)).text
        third = self.driver.find_element(By.XPATH, self.get_product_name_topN(2)).text
        result['first'] = first
        result['second'] = second
        result['third'] = third
        return result
    
    def get_top3_price_list(self) -> list:
        result = []
        first = self.driver.find_element(By.XPATH, self.get_price_topN(0)).text
        first = int(re.sub(r'^0-9', first))
        second = self.driver.find_element(By.XPATH, self.get_price_topN(1)).text
        second = int(re.sub(r'^0-9', second))
        third = self.driver.find_element(By.XPATH, self.get_price_topN(2)).text
        third = int(re.sub(r'^0-9', third))

        result.append(first)
        result.append(second)
        result.append(third)
        
        return result
    
    def get_top3_rating_list(self) -> list:
        result = []
        first = self.driver.find_element(By.XPATH, self.get_rating_topN(0)).text
        second = self.driver.find_element(By.XPATH, self.get_rating_topN(1)).text
        third = self.driver.find_element(By.XPATH, self.get_rating_topN(2)).text

        result.append(first)
        result.append(second)
        result.append(third)
        
        return result

    def get_tags_list(self, tag_count: int) -> list:
        result = []
        # 선택된 태그 수 만큼 가져옴
        # ex) i == 0 -> 삼성전자
        # ex) i == 1 -> 4점 이상
        # ex) i == 2 -> 200,000원 ~ 2,000,000원
        for i in range(tag_count):
            tag = self.driver.find_element(self.get_filter_tag_N(i)).text
            if ',' in tag:
                tag = tag.replace(',', '')
            result.append(tag)
        
        return result
        

    def click_topN_product(self, n: int) -> None:
        self.driver.find_element(By.XPATH, self.get_product_name_topN(n)).click()
        
    def click_brand_filter(self, brand:str) -> None:
        self.driver.find_element(By.XPATH, self.get_filter_brandname(brand)).click()

    def click_rating_filter(self, star: int) -> None:  # 1 ~ 4
        self.driver.find_element(By.XPATH, self.get_rating_topN(star))