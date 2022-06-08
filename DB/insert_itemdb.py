from yaml import load, FullLoader
import requests
import pymysql
from pprint import pprint
import logging

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config

raw_to_colname = {'Artifact':'artifact', 'Artifact?':'is_artifact', 'Category':'category', 'Eastern Resource':'eastern_resource',  "Environment":"environment",\
    'Koda - Clothing':'koda_clothing', 'Koda - Clothing?':'is_koda_clothing',
    'Koda - Core':'koda_core', 'Koda - Eyes':'koda_eyes', 'Koda - Head':'koda_head', 'Koda - Mega?':'is_koda_mega', 'Koda - Weapon':'koda_weapon', 'Koda - Weapon?':'is_koda_weapon',\
    'Koda ID':'koda_id', 'Koda?':'is_koda', 'Northern Resource Tier':'northern_resource_tier', 'Sediment':'sediment', 'Southern Resource':'southern_resource',\
    'Western Resource':'western_resource', 'Environment Tier':'environment_tier', 'Koda':'koda',  "Plot":'plot', 'Sediment Tier':'sediment_tier',\
    'Eastern Resource Tier':'eastern_resource_tier','Western Resource Tier':'western_resource_tier', 'Southern Resource Tier':'southern_resource_tier',\
    'Northern Resource':'northern_resource'}

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
for token_ID in range(2700, 100000):
    #url = f"https://api.opensea.io/api/v1/asset/{asset_contract_address}/{token_ID}/?include_orders=false"
    url = f"https://api.opensea.io/api/v1/assets?token_ids={token_ID}&collection_slug=otherdeed&order_direction=desc&limit=20&include_orders=false"

    response = requests.get(url, headers=headers)
    response = response.json()['assets'][0]
    #try:
        #if "success" not in response:
    if response != []:
        value_list = list()
        column_list = ["id", "token_id", "asset_contract_address", "image_url", "image_preview_url", "image_thumbnail_url", "image_original_url", "external_link"]
        
        for col in column_list:
            if col not in ["asset_contract_address", 'id'] and response[col] is None:
                value_list.append("\'\'")
            elif col in ["id", "token_id"]:
                value_list.append(f"{response[col]}")
            elif col == "asset_contract_address":
                value_list.append(f"\'{response['asset_contract']['address']}\'")
            else:
                value_list.append(f"\'{response[col]}\'")

        for trait in response['traits']:
            #print(f"{trait['trait_type']} : {trait['value']}")
            if type(trait['value'])==str and '\'' in trait['value'] :
                trait['value'] = trait['value'].replace('\'','＇')
                #value_list.append(f"\'{response[col]}\'")
            column_list.append(raw_to_colname[trait['trait_type']])
            value_list.append(f"\'{trait['value']}\'")
        
        column_cmd = ", ".join(column_list)
        value_cmd = ", ".join(value_list)
        try:
            cursor.execute(f"INSERT INTO {db_name}.ITEM ({column_cmd}) VALUES ({value_cmd})")
            conn.commit()
        except  Exception as e:
            logger.error(e)
            # logger.exception(e)
        finally : pass
    else:
        print(token_ID)

    # except  Exception as e:
    #     column_cmd = ", ".join(column_list)
    #     value_cmd = ", ".join(value_list)

    #     print(f"INSERT INTO {db_name}.ITEM ({column_cmd}) VALUES ({value_cmd})")
    #     logger.error(e)
    #     raise
    #     #logger.exception(e)
    #finally: pass