import streamlit as st
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import time
import urllib.request
import requests
import pymysql.cursors
from PIL import Image
from model import make_sim, pro_sim
from yaml import load, FullLoader
from io import BytesIO, StringIO
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader, Dataset, random_split
from st_clickable_images import clickable_images
# from model import nft_dataset, linear_model, save_model, Train, get_prediction


def increment_counter():
    st.session_state.token_num += 1

def decreasement_counter():
    st.session_state.token_num -= 1

def change_counter(num):
    st.session_state.token_num=num

def select_NFT(NFT):
    st.session_state.NFT_name=NFT

st.set_page_config(
    # layout="wide", 
    initial_sidebar_state="expanded",    # 사이드바 상태 : auto / expanded / collapsed
    page_title='King of 부동산', 
    page_icon='https://img.seadn.io/files/ba4845e224bcdea2f7a83318a1933534.png?auto=format'
    )

if 'NFT_name' not in st.session_state:
    st.session_state.NFT_name='Main'


# sidebar
st.session_state.NFT_name = st.sidebar.selectbox('Please select in selectbox!',
        ('Main','Otherdeed for Otherside', 'Azuki', 'Bored Ape Yacht Club','Test'))

if st.session_state.NFT_name == 'Main':
    st.header('저희는 다음과 같은 NFT를 지원합니다!!!')
    st.write('')
    st.write('')
    st.write('')

    Main_column0=st.columns(2)
    with Main_column0[0]:
        st.subheader('Otherdeed for Otherside')
        st.image('https://lh3.googleusercontent.com/yIm-M5-BpSDdTEIJRt5D6xphizhIdozXjqSITgK4phWq7MmAU3qE7Nw7POGCiPGyhtJ3ZFP8iJ29TFl-RLcGBWX5qI4-ZcnCPcsY4zI=s168')
    with Main_column0[1]:
        st.subheader('Azuki')
        st.image('https://lh3.googleusercontent.com/H8jOCJuQokNqGBpkBN5wk1oZwO7LM8bNnrHCaekV2nKjnCqw6UB5oaH8XyNeBDj6bA_n1mjejzhFQUP3O1NfjFLHr3FOaeHcTOOT=s168')
    
    Main_column1=st.columns(2)
    with Main_column1[0]:
        st.subheader('Bored Ape Yacht Club')
        st.image('https://lh3.googleusercontent.com/Ju9CkWtV-1Okvf45wo8UctR-M9He2PjILP0oOvxE89AyiPPGtrR3gysu1Zgy0hjd2xKIgjJJtWIc0ybj4Vd7wv8t3pxDGHoJBzDB=s168')


# Otherdeed for Otherside의 경우
if st.session_state.NFT_name == 'Otherdeed for Otherside':
    if 'token_num' not in st.session_state:
        st.session_state.token_num = -1

 
    def load_config(config_path:str):
        with open(config_path, "r") as f:
            config = load(f, FullLoader)
        return config

    config = load_config(config_path="C:/Users/user/Desktop/exercise/Final/dev_config.yaml")

    # # DB 연결
    # host=config['aws_db']['host']
    # user=config['aws_db']['user']
    # password=config['aws_db']['password']
    # port=config['aws_db']['port']
    # db_name=config['aws_db']['database']
    # conn = pymysql.connect(host=host, user=user, password=password, db=db_name, port=port,charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

    # # mysql 연결
    # host1=config['gcp_db']['host']
    # user1=config['gcp_db']['user']
    # password1=config['gcp_db']['password']
    # port1=config['gcp_db']['port']
    # db_name1 = config['gcp_db']['database']
    # conn1 = pymysql.connect(host=host1, user=user1, password=password1, db=db_name, port=port1, charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    

    # sql='select * from nftdb.ITEM'    # ITEM / TRADE / TRADE_test
    # curs=conn.cursor()
    # curs.execute(sql)
    # data=curs.fetchall()
    # data_dataframe=pd.DataFrame(data)
    # data_dataframe


    # sql1='select * from nftdb.TRADE'    # ITEM / TRADE / TRADE_test / PRICE_OFFER
    # curs1=conn.cursor()
    # curs1.execute(sql1)
    # data1=curs1.fetchall()
    # data_dataframe1=pd.DataFrame(data1)
    # data_dataframe1

    # sql2='select * from nftdb.PRICE_OFFER'    # ITEM / TRADE / TRADE_test / PRICE_OFFER
    # curs2=conn1.cursor()
    # curs2.execute(sql2)
    # data2=curs2.fetchall()
    # data_dataframe2=pd.DataFrame(data2)
    # data_dataframe2

    # ITEM
    if 'data_dataframe' not in st.session_state:
        st.session_state.data_dataframe=pd.read_csv('C:/Users/user/Desktop/exercise/Final/ITEM_dataframe.csv')

    # TRADE
    if 'data_dataframe1' not in st.session_state:
        st.session_state.data_dataframe1=pd.read_csv('C:/Users/user/Desktop/exercise/Final/TRADE_dataframe.csv')

    # PRICE_OFFER
    if 'data_dataframe' not in st.session_state:
        st.session_state.data_dataframe2=pd.read_csv('C:/Users/user/Desktop/exercise/Final/PRICE_OFFER_dataframe.csv')

    if 'sim_dataframe' not in st.session_state:
        st.session_state.sim_dataframe=pd.read_csv('C:/Users/user/Desktop/exercise/Final/sim_dataframe.csv',index_col=0)
    
    st.title("Otherdeed for Otherside")

    
    
    ordinal_number = ['첫', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
    
    token_columns=['artifact', 'is_artifact', 'category', 'eastern_resource', 'environment', 'koda_clothing', 'is_koda_clothing', 'koda_core', 'koda_eyes', 
    'koda_head', 'is_koda_mega', 'koda_weapon', 'is_koda_weapon', 'koda_id', 'is_koda', 'northern_resource', 'sediment', 'southern_resource', 'western_resource', 
    'easteren_resource', 'environment_tier', 'koda', 'northern_resource_tier', 'plot', 'sediment_tier', 'southern_resource_tier', 'western_resource_tier', 
    'eastern_resource_tier']
    
    token_price = ["41", "44.44", "41","44.44","44.44","44.44","44.44","44.44","44.44","44.44"]

    

    st.subheader('찾고 싶은 아이템을 입력해 주세요!!!')

    select_c=st.columns((4,1))

    with select_c[0]:
        st.session_state.select_text = st.text_input('Feature name','Token ID를 입력해주세요...')
    

    with select_c[1]:
        st.write('')
        st.write('')
        st.write('')
        st.session_state.select_button = st.button('Search')
    if st.session_state.select_button:
        if int(st.session_state.select_text) in st.session_state.data_dataframe['token_id'].values:
            st.session_state.idx=int(np.where(st.session_state.data_dataframe['token_id'].values==int(st.session_state.select_text))[0])
            st.session_state.token_num=10
        else:
            st.warning('해당 Token_id가 없습니다. 다시 입력해주세요.')
    


    if (st.session_state.token_num>=0) and (st.session_state.token_num<=9):
        st.header(f'오늘의 {ordinal_number[st.session_state.token_num]} 번째 추천 #{st.session_state.data_dataframe.loc[st.session_state.token_num][1]} : {token_price[st.session_state.token_num]} ETH')

        main_c = st.columns(2)
        with main_c[0]:
            st.image(st.session_state.data_dataframe.loc[st.session_state.token_num][6])
        with main_c[1]:
            st.write({token_columns[a]:str(list(st.session_state.data_dataframe.loc[st.session_state.token_num])[a+8]) for a in range(len(token_columns)) if str(st.session_state.data_dataframe.loc[st.session_state.token_num][a+8])!='nan'})
            
        sub_c = st.columns((4,3,3))
        with sub_c[0]:
            left_button = st.button(
                label="이전", disabled=(st.session_state.token_num<=0),
                on_click=decreasement_counter
            )
        with sub_c[1]:
            right_button = st.button(
                label="다음", disabled=(st.session_state.token_num>=len(ordinal_number)-1),
                on_click=increment_counter
            )
    elif st.session_state.token_num==10:
        st.header(f"#{st.session_state.data_dataframe.iloc[st.session_state.idx][1]}에 대한 정보입니다.")
        st.subheader(f'추천 가격 : {token_price[0]} ETH')

        main_c = st.columns(2)
        with main_c[0]:
            st.image(st.session_state.data_dataframe.loc[st.session_state.idx][6])
        with main_c[1]:
            st.write({token_columns[a]:str(list(st.session_state.data_dataframe.loc[st.session_state.idx])[a+8]) for a in range(len(token_columns)) if str(st.session_state.data_dataframe.loc[st.session_state.idx][a+8])!='nan'})
        back_col=st.columns(8)
        with back_col[7]:
            st.session_state.back_button=st.button('Back',on_click=change_counter,args=(-1,))

        # 유사한 item 10가지 추출
        # sim_dataframe=make_sim(data_dataframe)
        # sim_dataframe

        if 'sim_array' not in st.session_state:
            st.session_state.sim_array=pro_sim(st.session_state.sim_dataframe,st.session_state.idx)
    
    if st.session_state.token_num!=10:
        st.subheader('오늘의 추천 상품입니다!!!')
        col0, col1, col2, col3, col4= st.columns(5)
        with col0:
            # st.subheader(f'#{data_dataframe.loc[0][1]}')
            st.session_state.button0=st.button(label=f'#0',on_click=change_counter,args=(0,))
            st.image(st.session_state.data_dataframe.loc[0][6])
            st.caption(f"가격 : {token_price[0]} ETH")
            # response = requests.get(data_dataframe.loc[0][6])
            # response = requests.get(data_dataframe.loc[0][6])
            # img = Image.open(BytesIO(response.content))
            # st.button(f'{st.image(image=img,output_format="PNG")}')
            # st.button(f'{st.image(data_dataframe.loc[0][6],clamp=False,output_format="PNG")}')
            
        with col1:
            # st.subheader(f'#{data_dataframe.loc[1][1]}')
            st.session_state.button1=st.button(label=f'#1',on_click=change_counter,args=(1,))
            st.image(st.session_state.data_dataframe.loc[1][6])
            st.caption(f"가격 : {token_price[1]} ETH")

        with col2:
            # st.subheader(f'#{data_dataframe.loc[2][1]}')
            st.session_state.button2=st.button(label=f'#2',on_click=change_counter,args=(2,))
            st.image(st.session_state.data_dataframe.loc[2][6])
            st.caption(f"가격 : {token_price[2]} ETH")

        with col3:
            # st.subheader(f'#{data_dataframe.loc[3][1]}')
            st.session_state.button3=st.button(label=f'#3',on_click=change_counter,args=(3,))
            st.image(st.session_state.data_dataframe.loc[3][6])
            st.caption(f"가격 : {token_price[3]} ETH")

        with col4:
            # st.subheader(f'#{data_dataframe.loc[4][1]}')
            st.session_state.button4=st.button(label=f'#4',on_click=change_counter,args=(4,))
            st.image(st.session_state.data_dataframe.loc[4][6])
            st.caption(f"가격 : {token_price[4]} ETH")

        col5, col6, col7, col8, col9= st.columns(5)
        with col5:
            # st.subheader(f'#{data_dataframe.loc[5][1]}')
            st.session_state.button5=st.button(label=f'#5',on_click=change_counter,args=(5,))
            st.image(st.session_state.data_dataframe.loc[5][6])
            st.caption(f"가격 : {token_price[5]} ETH")

        with col6:
            # st.subheader(f'#{data_dataframe.loc[6][1]}')
            st.session_state.button6=st.button(label=f'#6',on_click=change_counter,args=(6,))
            st.image(st.session_state.data_dataframe.loc[6][6])
            st.caption(f"가격 : {token_price[6]} ETH")

        with col7:
            # st.subheader(f'#{data_dataframe.loc[7][1]}')
            st.session_state.button7=st.button(label=f'#7',on_click=change_counter,args=(7,))
            st.image(st.session_state.data_dataframe.loc[7][6])
            st.caption(f"가격 : {token_price[7]} ETH")

        with col8:
            # st.subheader(f'#{data_dataframe.loc[8][1]}')
            st.session_state.button8=st.button(label=f'#8',on_click=change_counter,args=(8,))
            st.image(st.session_state.data_dataframe.loc[8][6])
            st.caption(f"가격 : {token_price[8]} ETH")

        with col9:
            # st.subheader(f'#{data_dataframe.loc[9][1]}')
            st.session_state.button9=st.button(label=f'#9',on_click=change_counter,args=(9,))
            st.image(st.session_state.data_dataframe.loc[9][6])
            st.caption(f"가격 : {token_price[9]} ETH")







if st.session_state.NFT_name == 'Azuki':
    st.title("NFT Recommendation")
    st.header("Azuki")

    # 첫 번째 방식
    token_lists = ["#0595", "#2239", "#9024"]
    token_urls = [
        "https://img.seadn.io/files/ba4845e224bcdea2f7a83318a1933534.png?auto=format",
        "https://img.seadn.io/files/b9e7a129ca92b67d25e25488a1c2e21a.png?auto=format",
        "https://img.seadn.io/files/47a9498adb5f3e124828c3008c51a19b.png?auto=format"
    ]

    if 'token_num' not in st.session_state:
        st.session_state.token_num = 0
    
    c1, c2, c3 = st.columns((1, 10, 2))

    with c2:
        st.image(token_urls[st.session_state.token_num])
        st.caption(token_lists[st.session_state.token_num])
    with c1:
        for _ in range(15):
            st.write('')
        left_button = st.button(
            label="<", disabled=(st.session_state.token_num<=0),
            on_click=decreasement_counter
        )
    with c3:
        for _ in range(15):
            st.write('')
        right_button = st.button(
            label=">", disabled=(st.session_state.token_num>=len(token_lists)-1),
            on_click=increment_counter
        )
    


    # 두 번째 방식
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader("#0595")
        st.image("https://img.seadn.io/files/ba4845e224bcdea2f7a83318a1933534.png?auto=format")
        st.caption("property is %%%%")

    with col2:
        st.subheader("#2239")
        st.image("https://img.seadn.io/files/b9e7a129ca92b67d25e25488a1c2e21a.png?auto=format")

    with col3:
        st.subheader("#9024")
        st.image("https://img.seadn.io/files/47a9498adb5f3e124828c3008c51a19b.png?auto=format")

    with col4:
        st.subheader("#0000")
        st.image("https://img.seadn.io/files/ba4845e224bcdea2f7a83318a1933534.png?auto=format")

    with col5:
        st.subheader("#0000")
        st.image("https://img.seadn.io/files/ba4845e224bcdea2f7a83318a1933534.png?auto=format")