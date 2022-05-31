import pymysql
from yaml import load, FullLoader
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def load_config(config_path:str):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config

config = load_config(config_path="dev_config.yaml")
host=config['gcp_db']['host']
user=config['gcp_db']['user']
password=config['gcp_db']['password']
db = config['gcp_db']['database']
port=config['gcp_db']['port']
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding = 'utf-8'
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# def db_connect():
#     """
#     connect to database 
#     return cursor
#     """
    
#     # mysql 연결
#     db_name = config['gcp_db']['database']
#     conn = pymysql.connect(host=config['gcp_db']['host'], user=config['gcp_db']['user'], password=config['gcp_db']['password'], db=db_name, port=config['gcp_db']['port'], charset='utf8')
#     cursor = conn.cursor()
#     return cursor

