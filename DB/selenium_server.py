# https://2bmw3.tistory.com/31?category=946986

import requests
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver import ActionChains

# 이더스캔 토큰정보 크롤링 함수

URL = "https://opensea.io/collection/otherdeed/activity"


response = requests.get(url=URL)
options = webdriver.ChromeOptions()
# 크롬드라이버 헤더 옵션추가 (리눅스에서 실행시 필수)
options.add_argument('window-size=1920,1080')
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 크롬드라이버 경로
driver_path = './chromedriver'
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

### 추가된 부분 ###
# selenium stealth 옵션추가 ( cloudflare 우회용 )
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
### // 추가된 부분 ###

driver.get('https://opensea.io/collection/otherdeed/activity')
#driver.get('https://naver.com')
time.sleep(20)

scroll_element = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[5]/div/div[4]/div[3]/div[3]/div[3]/div/div[2]/div[9]')
action = ActionChains(driver)
action.move_to_element(scroll_element).perform()

for idx in range(1, 18):
    age= driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div/div/div[5]/div/div[4]/div[3]/div[3]/div[3]/div/div[2]/div[{idx}]/button/div/div[7]/div/a").text
    age = age.strip().split(" ")
    age = " ".join(age[:-1])
                                        
    if "minute" in age or "second" in age:
        link = driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div/div/div[5]/div/div[4]/div[3]/div[3]/div[3]/div/div[2]/div[{idx}]/button/div/div[2]/div/div/div/div[2]/span[2]/a")
        link = link.get_attribute("href").strip().split("/")
        token_id = link[-1]                                                  

        price = driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div/div/div[5]/div/div[4]/div[3]/div[3]/div[3]/div/div[2]/div[{idx}]/button/div/div[3]/div/div[1]/div/div[2]")
        price = price.text

        price_type_link = driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div/div/div[5]/div/div[4]/div[3]/div[3]/div[3]/div/div[2]/div[{idx}]/button/div/div[3]/div/div[1]/div/div[1]/a")
        price_type_link = price_type_link.get_attribute("href")
        if "etherscan" in price_type_link : price_type = "ETH"
        elif "WETH" in price_type_link : price_type = "WETH"

        dollor = driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div/div/div[5]/div/div[4]/div[3]/div[3]/div[3]/div/div[2]/div[{idx}]/button/div/div[3]/div/div[2]/span/div/div").text

        print("=================================")
        print(token_id, price, price_type, dollor, age)

driver.close()
