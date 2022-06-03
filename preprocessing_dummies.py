import pymysql
from yaml import load, FullLoader
import pandas as pd
import time
from datetime import datetime
import numpy as np

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config

config = load_config(config_path="dev_config.yaml")

# mysql 연결
db_name = config['gcp_db']['database']
conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
cursor = conn.cursor()

# trade 불러오기
cursor.execute("Select * from nftdb.TRADE")
data=cursor.fetchall() 
trade=pd.DataFrame(data)

# item 불러오기
cursor.execute("Select * from nftdb.ITEM")
data2=cursor.fetchall() 
item=pd.DataFrame(data2)

# timestamp
timestamp = []
for i in trade[1]:
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
for i in trade[10]:
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
for i in trade[7]:
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
item_price=price_27_time[[5,'eth_price']]

del item[21]
del item[29]
del item[31]

item_property = pd.concat([item[1],item.loc[:,8:35]],axis=1)
item_property = item_property.rename(columns={1:'id'})
item_price = item_price.rename(columns={5:'id'})
all_item_property_dummy = pd.get_dummies(item_property.iloc[:,1:])
all_item = pd.concat([item_property.iloc[:,0],all_item_property_dummy], axis=1)
property_price = pd.merge(all_item,item_price,on='id')
df = pd.DataFrame(property_price.values)
df.to_csv('property_dummy.csv')
df2 = pd.DataFrame(all_item.values)
df2.to_csv('all_property_dummy.csv')