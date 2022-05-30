from yaml import load, FullLoader
import pymysql
import logging
import requests
import time

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config


config = load_config(config_path="dev_config.yaml")

# mysql 연결
db_name = config['gcp_db']['database']
conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
cursor = conn.cursor()

# api 
asset_contract_address = "0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258"
headers = {
    "Accept": "application/json",
    "X-API-KEY": config['opensea']['key']
}
logger = logging.getLogger()

for token_ID in range(53117, 100000):
    columns_list = list()
    values_list = list()

    columns_list.append('Token_ID')
    columns_list.append('Asset_contract_address')
    values_list.append(f"{token_ID}")
    values_list.append(f"\'{asset_contract_address}\'")

    # 구매자
    buyer_url = f"https://api.opensea.io/wyvern/v1/orders?asset_contract_address={asset_contract_address}&is_english=false&bundled=false&include_bundled=false&token_ids={token_ID}&side=0&limit=1&offset=0&order_by=eth_price&order_direction=desc"
    buyer_response = requests.get(buyer_url, headers=headers)
    if buyer_response.json()['orders'] != []:
        buyer_response = buyer_response.json()['orders'][0]
        buyer_price = float(buyer_response['current_price'])*0.000000000000000001
        buyer_price_type = buyer_response['payment_token_contract']['name']
        
        columns_list.append('Buyer_price')
        columns_list.append('Buyer_price_type')
        values_list.append(f"{buyer_price}")
        values_list.append(f"\'{buyer_price_type}\'")

    time.sleep(1)

    # 판매자
    seller_url = f"https://api.opensea.io/wyvern/v1/orders?asset_contract_address={asset_contract_address}&bundled=false&include_bundled=false&token_ids={token_ID}&side=1&limit=20&offset=0&order_by=created_date&order_direction=desc"
    seller_response = requests.get(seller_url, headers=headers)
    if seller_response.json()['orders'] != []:
        seller_response = seller_response.json()['orders'][0]
        seller_price = float(seller_response['current_price'])*0.000000000000000001
        seller_price_type = seller_response['payment_token_contract']['name']
        
        columns_list.append('Seller_price')
        columns_list.append('Seller_price_type')
        values_list.append(f"{seller_price}")
        values_list.append(f"\'{seller_price_type}\'")

    time.sleep(1)

    columns_cmd = ",".join(columns_list)
    values_cmd = ",".join(values_list)

    print(f"INSERT INTO {db_name}.PRICE_OFFER ({columns_cmd}) VALUES ({values_cmd})")

    try:
        cursor.execute(f"INSERT INTO {db_name}.PRICE_OFFER ({columns_cmd}) VALUES ({values_cmd})")
        conn.commit()
    except  Exception as e:
        logger.error(e)
        #logger.exception(e)
    finally : pass

