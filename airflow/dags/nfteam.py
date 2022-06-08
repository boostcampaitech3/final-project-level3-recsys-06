
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import requests
import pandas as pd
import numpy as np
import time
import pymysql
import datetime


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from torch.utils.data import Dataset, DataLoader, random_split
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver import ActionChains
from yaml import load, FullLoader
from copy import deepcopy
from torchmetrics import MeanAbsolutePercentageError
from queue import PriorityQueue


current_dir = '/opt/ml/level3-product-serving-level3-recsys-06/airflow/dags/'

#model
class linear_model(nn.Module):
    def __init__(self, num_column):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(num_column-2,num_column-2),
            nn.Linear(num_column-2,(num_column-2)//2),
            nn.Linear((num_column-2)//2,(num_column-2)//4),
            nn.Linear((num_column-2)//4,(num_column-2)//8),
            nn.Linear((num_column-2)//8,1)
        )
    def forward(self, data):
        return self.model(data)

#dataset
class nft_dataset(Dataset):
    def __init__(self,data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx,1:-1]
        y = self.data[idx,-1].view(1)
        return x,y

class all_dataset(Dataset):
    def __init__(self,data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx,1:]
        return x


def save_model(model, saved_dir, file_name):
    os.makedirs(saved_dir, exist_ok=True)
    check_point = {
        'net': model.state_dict()
    }
    output_path = os.path.join(saved_dir, file_name)
    torch.save(check_point,output_path)

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config

# # https://2bmw3.tistory.com/31?category=946986
def input_opensea_trade_data():

    # mysql 연결
    config = load_config(config_path="dev_config.yaml")

    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
    cursor = conn.cursor()

    URL = "https://opensea.io/collection/otherdeed/activity"
    response = requests.get(url=URL)
    
     # 크롬드라이버 경로
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver_path = './chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

     # selenium stealth 옵션추가 ( cloudflare 우회용 )
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    driver.get(url=URL)
    driver.get('https://opensea.io/collection/otherdeed/activity')
    time.sleep(5)

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
            #print(token_id, price, price_type, dollor, age)
            cmd = f"INSERT INTO {db_name}.TRADE_new (age, token_id, price, input_datetime) VALUES (\'{age}\', {token_id}, \'{price} {price_type}\', now())"
            print(cmd)
            cursor.execute(cmd)
            conn.commit()

    driver.close()
    conn.close()

def input_looksrare_trade_data():

    # mysql 연결
    config = load_config(config_path="dev_config.yaml")

    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
    cursor = conn.cursor()


    URL = "https://looksrare.org/collections/0x34d85c9CDeB23FA97cb08333b511ac86E1C4E258?queryID=811958bc6c14784a73cf8aae24bdbcb3&queryIndex=prod_tokens#activity"
    response = requests.get(url=URL)
    
     # 크롬드라이버 경로
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver_path = './chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

     # selenium stealth 옵션추가 ( cloudflare 우회용 )
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    driver.get(url=URL)
    time.sleep(5)

    sale_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div[3]/div[1]/div[4]/div[3]/span/div/div[2]/div/div/button[3]")
    sale_button.click()
    time.sleep(3)

    for idx in range(1, 6):
        age = driver.find_element_by_xpath(f"/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[3]/div[{idx}]/div/div[4]/div/a").text
        age = age.strip().split(" ")
        age = " ".join(age[:-1])
                                      
        if "minute" in age or "second" in age:
                                                    
            token_id = driver.find_element_by_xpath(f"/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[3]/div[{idx}]/div/div[2]/div/div/ul/div/a/button/div").text
            token_id = token_id.strip().split(" ")
            token_id = token_id[-1]
            token_id = token_id[1:]

            price = driver.find_element_by_xpath(f"/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[3]/div[{idx}]/div/div[3]/div/div[1]/div").text
            price_type = "WETH"
            dollor = "$ 1000"
            
            print("=================================")
            # print(token_id, price, price_type, dollor, age)
            cmd = f"INSERT INTO {db_name}.TRADE_new (age, token_id, price, input_datetime) VALUES (\'{age}\', {token_id}, \'{price} {price_type}\', now())"
            print(cmd)
            cursor.execute(cmd)
            conn.commit()

    driver.close()
    conn.close()

def input_x2y2_trade_data():

    # mysql 연결
    config = load_config(config_path="dev_config.yaml")

    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
    cursor = conn.cursor()


    URL = "https://x2y2.io/collection/otherdeed/activities"
    response = requests.get(url=URL)
    
     # 크롬드라이버 경로
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver_path = './chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

     # selenium stealth 옵션추가 ( cloudflare 우회용 )
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    driver.get(url=URL)
    time.sleep(10)


    for idx in range(1, 6):
        age = driver.find_element_by_xpath(f"/html/body/div[1]/div/div[3]/div[3]/div[2]/div[3]/div[1]/div[{idx}]/div/div[2]/div[3]/a/span/span").text
        age = age.strip().split(" ")
        age = " ".join(age[:-1])
                                      
        if "minute" in age or "second" in age:
                                                    
            token_id = driver.find_element_by_xpath(f"/html/body/div[1]/div/div[3]/div[3]/div[2]/div[3]/div[1]/div[{idx}]/div/div[1]/div[2]/div[1]/div[1]/a").text
            token_id = token_id[1:]

            price = driver.find_element_by_xpath(f"/html/body/div[1]/div/div[3]/div[3]/div[2]/div[3]/div[{idx}]/div[1]/div/div[1]/div[2]/div[2]/div/p").text

            price_type_color = driver.find_element_by_xpath(f"/html/body/div[1]/div/div[3]/div[3]/div[2]/div[3]/div[1]/div[{idx}]/div/div[1]/div[2]/div[2]/div")
            price_type_color = price_type_color.find_element_by_tag_name('svg')
            if price_type_color.find_elements_by_tag_name('g') != []:
                price_type_color = price_type_color.find_element_by_tag_name('g')
                price_type_color = price_type_color.find_element_by_tag_name('path')
            else  : 
                price_type_color = price_type_color.find_elements_by_tag_name('path')[1]
            price_type_color = price_type_color.get_attribute("fill")
        

            if price_type_color == "#141416":
                price_type = "ETH"
            elif price_type_color == "#DF5960":
                price_type = "WETH"
                    
            print("=================================")
            #print(token_id, price, price_type, age)
            cmd = f"INSERT INTO {db_name}.TRADE_new (age, token_id, price, input_datetime) VALUES (\'{age}\', {token_id}, \'{price} {price_type}\', now())"
            print(cmd)
            cursor.execute(cmd)
            conn.commit()

    driver.close()
    conn.close()


def item_preprocessing():
    config = load_config(config_path="dev_config.yaml")

# mysql 연결
    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    # trade 불러오기
    cursor.execute(f"Select * from {db_name}.TRADE_new")
    data=cursor.fetchall() 
    trade=pd.DataFrame(data)

    # item 불러오기
    cursor.execute(f"Select * from {db_name}.ITEM")
    data2=cursor.fetchall() 
    item=pd.DataFrame(data2)

    # timestamp
    timestamp = []
    #for i in trade['Age']:
    for i in trade['age']:
        t=0
        for j in range(len(i.split())-2):
            if i.split()[j+1] == 'days' or i.split()[j+1] == 'day':
                t += int(i.split()[j])*24*60*60
            elif i.split()[j+1] == 'hrs' or i.split()[j+1] == 'hr':
                t += int(i.split()[j])*60*60
            elif i.split()[j+1] == 'mins' or i.split()[j+1] == 'min':
                t += int(i.split()[j])*60
        timestamp.append(t)

    crawling_time=[]
    #for i in trade['Input_datetime']:
    for i in trade['input_datetime']:
        t = time.mktime(i.timetuple())
        crawling_time.append(t)
    
    trade_time = np.array(crawling_time)-np.array(timestamp)
    trade['trade_time'] = trade_time

    trade_time2=[]
    for i in trade['trade_time']:
        trade_time2.append(datetime.fromtimestamp(i))

    trade['trade_time2'] = trade_time2

    # eth 가격
    eth_price=[]
    eth_exist=[]
    #for i in trade['Price']:
    for i in trade['price']:
        if ('WETH' or 'ETH') in i :
            eth_exist.append(True)
            eth_price.append(float(i.split()[0]))
        else:
            eth_exist.append(False)

    eth_exist_trade = trade[eth_exist].copy()
    eth_exist_trade['eth_price'] = eth_price

    # 이상치 제거
    price_27=eth_exist_trade[np.logical_and(eth_exist_trade['eth_price']<27,eth_exist_trade['eth_price']>2.5)]
    price_27_time = price_27[price_27['trade_time']>1.6518*1e9]

    # item 특성과 가격 합치기
    #item_price=price_27_time[['Token_ID','eth_price']]
    item_price=price_27_time[['token_id','eth_price']]
    item_price

    del item['koda_id']
    del item['koda']
    del item['plot']

    item_property = pd.concat([item['token_id'],item.loc[:,'artifact':'eastern_resource_tier']],axis=1)
    all_item_property_dummy = pd.get_dummies(item_property.iloc[:,1:])
    item_price = item_price.rename(columns={'Token_ID':'token_id'})
    all_item_property_dummy = pd.get_dummies(item_property.iloc[:,1:])
    all_item = pd.concat([item_property.iloc[:,0],all_item_property_dummy], axis=1)
    property_price = pd.merge(all_item,item_price,on=['token_id'])
    df = pd.DataFrame(property_price.values)
    df.to_csv(os.path.join(current_dir, 'property_dummy.csv'), index=False)
    df2 = pd.DataFrame(all_item.values)
    df2.to_csv(os.path.join(current_dir, 'all_property_dummy.csv'), index=False)
   
def train():

    data = pd.read_csv(os.path.join(current_dir, 'property_dummy.csv')) # 데이터 전처리 후 추가
    num_column = data.shape[1]
    data = data.to_numpy()
    data = torch.tensor(data, dtype=torch.float32)

    all_data = pd.read_csv(os.path.join(current_dir, 'all_property_dummy.csv'))
    all_data = all_data.to_numpy()
    all_data = torch.tensor(all_data, dtype=torch.float32)

    trainset = nft_dataset(data)
    #all_set = all_dataset(all_data)


    #dataloader
    train_loader = DataLoader(
        trainset,
        batch_size=32,
        num_workers=0,
        shuffle=True
    )


    model=linear_model(num_column=num_column)
    device = torch.device('cuda')
    model.to(device)

    #criterion,optimizer

    # criterion = nn.MSELoss()
    criterion = MeanAbsolutePercentageError().to(device)
    optimizer = optim.Adam(model.parameters())

    # train
    epochs= 50
    model.train()
    min_loss = np.inf
    loss_list=[]
    for epoch in tqdm(range(epochs)):
        running_loss = 0
        for i, data in enumerate(train_loader):
            x, y = data
            x, y = x[0].cuda() , y[0].cuda()
            optimizer.zero_grad()
            outputs = model(x)
            loss = criterion(outputs, y)
            running_loss += loss
            loss.backward()
            optimizer.step()
        if running_loss < min_loss:
            min_loss = running_loss
            best_model = deepcopy(model.state_dict())
            save_model(model, os.path.join(current_dir), 'model.pt')


    print("train Done!")

def predict():

    config = load_config(config_path="dev_config.yaml")

    # mysql 연결
    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
    cursor = conn.cursor()


    data = pd.read_csv(os.path.join(current_dir, 'property_dummy.csv'))  # 데이터 전처리 후 추가
    num_column = data.shape[1]
    data = data.to_numpy()
    data = torch.tensor(data, dtype=torch.float32)

    all_data = pd.read_csv(os.path.join(current_dir, 'all_property_dummy.csv'))
    all_data = all_data.to_numpy()
    all_data = torch.tensor(all_data, dtype=torch.float32)

    #trainset = nft_dataset(data)
    all_set = all_dataset(all_data)


    num_column = data.shape[1]
    model=linear_model(num_column=num_column)

    device = torch.device('cuda')
    model_path = os.path.join(current_dir,'model.pt')
    checkpoint = torch.load(model_path,map_location=device)
    state_dict = checkpoint['net']
    model.load_state_dict(state_dict)

    
    all_loader = DataLoader(
        all_set,
        batch_size=1,
        num_workers=0,
        shuffle=False
    )

    with torch.no_grad():
        model.to(device)
        model.eval()
        pred_list=[]
        y_list=[]
        for val_batch in all_loader:
            x = val_batch
            x = x[0].to(device)
            outputs = model(x)
            pred_list.append(outputs.item())

    result = pd.DataFrame(pred_list)
    result.to_csv(os.path.join(current_dir, 'result_nfteam.csv'), index=False)

    for token_id, predict_value in tqdm(zip(range(100000), pred_list)):
        cmd = f"UPDATE {db_name}.ITEM SET predict_value={predict_value} WHERE token_id={token_id}"
        cursor.execute(cmd)
        conn.commit()
    
    conn.close()

def rec_10_nft():
    asset_contract_address = "0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258"

    rec_10 = PriorityQueue()

    config = load_config(config_path="dev_config.yaml")

    # mysql 연결
    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
    cursor = conn.cursor()

    cmd = f"SELECT {db_name}.ITEM.token_id, {db_name}.ITEM.predict_value, {db_name}.PRICE_OFFER.Seller_price, {db_name}.PRICE_OFFER.Seller_price_type, {db_name}.PRICE_OFFER.Buyer_price, {db_name}.PRICE_OFFER.Buyer_price_type " \
        + f"from {db_name}.ITEM left join {db_name}.PRICE_OFFER on {db_name}.ITEM.token_id={db_name}.PRICE_OFFER.Token_ID"

    cursor.execute(cmd)
    data=cursor.fetchall() 
    predict_price = pd.DataFrame(data)

    # apecoin , dai stablecoin 제거
    # 3은 Seller_price_type, 5는 Buyer_price_type
    predict_price.loc[predict_price[3]=='ApeCoin',2]=np.nan 
    predict_price.loc[predict_price[5]=='ApeCoin',4]=np.nan
    predict_price.loc[predict_price[5]=='Dai Stablecoin',4]=np.nan

    # 둘다 nan인 경우 제거
    eth_predict_price = predict_price[np.logical_not(np.logical_and(predict_price[2].isna(),predict_price[4].isna()))].loc[:,[0,1,2,4]]

    # 비교를 위해 nan값 0으로
    eth_predict_price=eth_predict_price.fillna(0)

    
    # 가격 차이 가장 큰거 10개
    rec10 = eth_predict_price.iloc[np.argpartition(eth_predict_price[1]-np.maximum(eth_predict_price[2],eth_predict_price[4]),-10)[-10:],:]

    # predict_price = predict_price.fillna(0)

    # #diff_list = list()
    # for i in tqdm(range(len(predict_price))):
    #     token_id, predict_value, seller_price, buyer_price = predict_price.loc[i, :]
    #     rec_10.put((-(predict_value-max(seller_price, buyer_price)), predict_value, token_id))
    
    for idx in range(10):
        token_id, predict_value = rec10.iloc[idx, 0], rec10.iloc[idx, 1]
        #print(token_id, predict_value)
        # _, predict_value, token_id = rec_10.get()
        cmd = f"INSERT INTO {db_name}.TOP_10_ITEMS VALUES (\'{asset_contract_address}\', {int(token_id)}, NOW(),  {predict_value})"
        print(cmd)
        cursor.execute(cmd)
        conn.commit()
    
    conn.close()


default_args = {
    'owner': 'hyeji',
    'depends_on_past': False,  # 이전 DAG의 Task가 성공, 실패 여부에 따라 현재 DAG 실행 여부가 결정. False는 과거의 실행 결과 상관없이 매일 실행한다
    'start_date': datetime(2022, 6, 5),
    'retires': 5,  # 실패시 재시도 횟수
    'retry_delay': timedelta(seconds=1)  # 만약 실패하면 5분 뒤 재실행
}


# with 구문으로 DAG 정의
with DAG(
        dag_id='nfteam',
        default_args=default_args,
        schedule_interval='0 */1 * * *',  # UTC 시간 기준 0시 30분에 Daily로 실행하겠다! 한국 시간 기준 오전 9시 30분
        tags=['test']
) as dag:
    # TRADE 데이터 갱신하기
    input_opensea_trade_step = PythonOperator(
        task_id="nft_input_opensea_trade",
        python_callable=input_opensea_trade_data
    )

    input_looksrare_trade_step = PythonOperator(
        task_id="nft_input_looksrare_trade",
        python_callable=input_looksrare_trade_data
    )

    input_x2y2_trade_step = PythonOperator(
        task_id="nft_input_x2y2_trade",
        python_callable=input_x2y2_trade_data
    )

    # 전처리하기
    preprocessing_step = PythonOperator(
        task_id="nft_preprocessing",
        python_callable=item_preprocessing
    )

    # 훈련
    train_step = PythonOperator(
        task_id="nft_model_train",
        python_callable=train
    )
 
    # 결과 뽑고 테이블에 넣기
    predict_step = PythonOperator(
        task_id="nft_model_predict",
        python_callable=predict
    )
    
    # 저평가된 아이템 10개 뽑기
    rec10_step = PythonOperator(
        task_id="nft_rec10",
        python_callable=rec_10_nft
    )
    
    input_opensea_trade_step >> input_looksrare_trade_step >> input_x2y2_trade_step >> preprocessing_step >> train_step >> predict_step >> rec10_step
