# https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-%EB%B4%87-%ED%83%90%EC%A7%80-%EC%9A%B0%ED%9A%8C/
# https://stackoverflow.com/questions/64165726/selenium-stuck-on-checking-your-browser-before-accessing-url

from pyathena import connect
from selenium import webdriver
import chromedriver_autoinstaller
import subprocess
import pymysql
import time
from yaml import load, FullLoader
import logging
#from datetime import datetime

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config

config = load_config(config_path="dev_config.yaml")

# mysql 연결
db_name = config['gcp_db']['database']
conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
cursor = conn.cursor()

# selenium 크롤링
subprocess.Popen(r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument("--disable-blink-features=AutomationControlled")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)


driver = webdriver.Chrome(executable_path='chromedriver', options=option)

# 크롤링할 URL
URL = f'https://etherscan.io/nfttracker?contractAddress=0x34d85c9CDeB23FA97cb08333b511ac86E1C4E258#trade'
driver.get(url=URL)
time.sleep(30)

select_rows = driver.find_element_by_xpath("/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[1]/div/label/select/option[4]")
select_rows.click()
time.sleep(3)

PAGE = 0
# for _ in range(PAGE):
#     next_page = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[2]/div/ul/li[4]/a')
#     next_page.click()
#     time.sleep(3)

logger = logging.getLogger()
for i in range(381-PAGE):
#for i in range(2):
    #print(i, end=" ")

    table = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div/div[3]/div[2]/table')
    tbody = table.find_element_by_tag_name("tbody")
    rows = tbody.find_elements_by_tag_name("tr")
    for index, value in enumerate(rows):
        body=value.find_elements_by_tag_name("td")
        print(f"INSERT INTO {db_name}.TRADE VAlUES ( \'{body[1].text}\', \'{body[2].text}\', \'{body[3].text}\', \'{body[4].text}\', \'{body[5].text}\', {body[6].text}, {body[7].text}, \'{body[8].text}\', \'{body[9].text}\', \'{body[10].text}\')")
        try:
            cursor.execute(f"INSERT INTO {db_name}.TRADE VAlUES (\'{body[1].text}\', \'{body[2].text}\', \'{body[3].text}\', \'{body[4].text}\', \'{body[5].text}\', {body[6].text}, {body[7].text}, \'{body[8].text}\', \'{body[9].text}\', \'{body[10].text}\', NOW())")
            conn.commit()
        except  Exception as e:
            logger.error(e)
            #logger.exception(e)
        finally: pass

    
    next_page = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[2]/div/ul/li[4]/a')
    next_page.click()

    time.sleep(3)




