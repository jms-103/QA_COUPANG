import pickle
import pytest
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import sys
import os

# 프로젝트 루트를 시스템 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="function")
def driver():
    # 쿠팡이 자동화 크롤링 막아놔서 많은 옵션수정이 필요하다.
    chrome_options = Options()  

    # 쿠팡 자동화로 열면 클릭 이후 자동화 동작 안하므로 아래와 같은 코드 삽입
    arg = ["user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/91.0",
           "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"]
    # 1) User-Agent 변경
    arg_index = randint(0, 1)
    chrome_options.add_argument(arg[arg_index])
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/91.0")
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # 2) SSL 인증서 에러 무시
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")

    # 4) Selenium이 automation된 브라우저임을 숨기는 몇 가지 설정
    #    - (disable-blink-features=AutomationControlled) 제거
    #    - excludeSwitches, useAutomationExtension
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 혹은 다음 방식으로 Blink 특징을 비활성화할 수도 있으나
    # "AutomationControlled" 자체가 표기되지 않도록 한다.
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 5) 디버그 로깅 줄이기 (선택)
    # chrome_options.add_argument("--log-level=3") 

    # 6) Sandbox나 DevShm 사이즈 문제 우회 (리눅스 환경에서 발생 가능)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    # 우리 쿠팡 url 타고 온거야
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"Referer": "https://www.coupang.com/"}})

    driver.execute_cdp_cmd("Network.clearBrowserCache", {})

    # 그런데 쓰다 ip 막힐 수 있음. ip막히지 않도록 잘 써야 함


    driver.implicitly_wait(5)

    

    yield driver

    driver.quit()




