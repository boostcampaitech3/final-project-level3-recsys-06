import pymysql
from yaml import load, FullLoader
import pandas as pd
import torch
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

# item 불러오기
cursor.execute("Select * from nftdb.ITEM")
data2=cursor.fetchall() 
item=pd.DataFrame(data2)

# 특성 dummies 만들기
del item[21] # koda_id
del item[29] # koda
del item[31] # plot

item_properties = item.loc[:,8:35]
A=pd.get_dummies(item_properties).values.astype(int)

device = torch.device('cuda')
A_tensor = torch.tensor(A, dtype=torch.int8)
A_T_tensor = torch.tensor(A.T, dtype=torch.int8)
A_tensor.to(device)
A_T_tensor.to(device)

# 유사도 구하기
similarity=[]
for i in range(99998):
    similarity.append(np.concatenate((np.array([0]*(i+1)),torch.mm(A_tensor[i,:].view(1,-1),A_T_tensor[:,i+1:]).numpy()),axis=None))
similarity.append(np.array([0]*(i+1)))
# 메모리 부족으로 한번에 안될시 나눠서 하고 합치기

similarity = np.array(similarity)
similarity = similarity + similarity.T
similarity.to_csv('similarity.csv')