import pymysql
from yaml import load, FullLoader

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config

def db_connect():
    """
    connect to database 
    return cursor
    """
    config = load_config(config_path="dev_config.yaml")
    # mysql 연결
    db_name = config['gcp_db']['database']
    conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
    cursor = conn.cursor()
    return cursor

