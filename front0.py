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

st.set_page_config(
    # layout="wide", 
    initial_sidebar_state="collapsed", 
    page_title='King of 부동산', 
    page_icon='https://img.seadn.io/files/ba4845e224bcdea2f7a83318a1933534.png?auto=format'
    )


# DB 연결
host=
user=
password=

conn = pymysql.connect(host=host, user=user, password=password, db='nftdb', charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

sql='select * from nftdb.ITEM'    # ITEM / TRADE / TRADE_test
curs=conn.cursor()
curs.execute(sql)
data=curs.fetchall()
data_dataframe=pd.DataFrame(data)
data_dataframe



'''
sql='select * from nftdb.TRADE'    # ITEM / TRADE / TRADE_test
curs1=conn.cursor()
curs1.execute(sql)
data1=curs1.fetchall()
data_dataframe1=pd.DataFrame(data1)
#data_dataframe1
'''



# # train
# ## dataload
# exer_data=pd.read_csv('C:/Users/user/Desktop/exercise/Final/test.csv',index_col=0)
# ## hyper parameter
# batch_size=1
# num_column=exer_data.shape[1]
# epochs=50
# ## dataset / dataloader
# exer_dataset=nft_dataset(exer_data)
# device=torch.device('cuda')
# model=linear_model(xdim=num_column-1,hdims=[16,32],ydim=1)
# # Train(model,exer_dataset,batch_size,epochs)

# # checkpoint=torch.load('',map_location=device)
# # state_dict=checkpoint['net']
# # model.load_state_dict(state_dict)
# # answer=get_prediction(model,)

# sidebar
NFT_name = st.sidebar.selectbox('Please select in selectbox!',
                      ('Otherdeed for Otherside', 'Azuki', 'test'))

# Otherdeed for Otherside의 경우
if NFT_name == 'Otherdeed for Otherside':
    st.title("Otherdeed for Otherside")
    
    ordinal_number = ['첫', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
    
    token_columns=['artifact', 'is_artifact', 'category', 'eastern_resource', 'environment', 'koda_clothing', 'is_koda_clothing', 'koda_core', 'koda_eyes', 
    'koda_head', 'is_koda_mega', 'koda_weapon', 'is_koda_weapon', 'koda_id', 'is_koda', 'northern_resource', 'sediment', 'southern_resource', 'western_resource', 
    'easteren_resource', 'environment_tier', 'koda', 'northern_resource_tier', 'plot', 'sediment_tier', 'southern_resource_tier', 'western_resource_tier', 
    'eastern_resource_tier']
    # token_urls = [
    #     "https://img.seadn.io/files/c4b801700179401a357ce65a4cbde641.jpg?auto=format",
    #     "https://img.seadn.io/files/933d82b7502678d751f79cfab2c29f75.jpg?auto=format",
    #     "https://img.seadn.io/files/d2264e9308bf071d6847280bac643430.jpg?auto=format"
    # ]
    token_price = ["41", "44.44", "41","44.44","44.44","44.44","44.44","44.44","44.44","44.44"]
    # token_property = [
    #     {'ARTIFACT':'Slime Juice 0.72%', 'ARTIFACT?': 'Yes 21%',
    #     'CATEGORY_Psychedelic':9, 'EASTERN RESOURCE_Phantom':0.07,
    #     'ENVIRONMENT_Shadow':2, 'KODA?_NO':90,
    #     'NORTHERN RESOURCE_Bonestone':3, 'SEDIMENT_Rainbow Atmos':22,
    #     'SOUTHERN RESOURCE_Runa':3, 'WESTERN RESOURCE_Gloomia':0.07},
    #     {'ARTIFACT?_No':79, 'CATEGORY_Volcanic':15,
    #     'EASTERN RESOURCE_Oblivion':3, 'ENVIRONMENT_Molten':5,
    #     'KODA?_No':90, 'SEDIMENT_Cosmic Dream':23,
    #     'WESTERN RESOURCE_Spikeweed':3},
    #     {'ARTIFACT?_No':79, 'CATEGORY_Volcanic':15,
    #     'EASTERN RESOURCE_Oblivion':3, 'ENVIRONMENT_Crimson':3,
    #     'KODA?_No':90, 'NORTHERN RESOURCE_Lumileaf':3,
    #     'SEDIMENT_Cosmic Dream':23}
    # ]

    if 'token_num' not in st.session_state:
        st.session_state.token_num = 0
        
    st.header(f'오늘의 {ordinal_number[st.session_state.token_num]} 번째 추천 #{data_dataframe.loc[st.session_state.token_num][1]} : {token_price[st.session_state.token_num]} ETH')

    main_c = st.columns(2)
    # with main_c[0]:
    #     st.image(token_urls[st.session_state.token_num])
    # with main_c[1]:
    #     st.subheader(f"{token_lists[st.session_state.token_num]}")
    #     st.write(f"가격 : {token_price[st.session_state.token_num]} ETH")
    #     st.write(token_property[st.session_state.token_num])

    with main_c[0]:
        st.image(data_dataframe.loc[st.session_state.token_num][6])
    with main_c[1]:
        # st.subheader(f"{data_dataframe.loc[st.session_state.token_num][1]}")
        # st.write(f"가격 : {30} ETH")
        st.write({token_columns[a]:list(data_dataframe.loc[st.session_state.token_num])[a+8] for a in range(len(token_columns)) if data_dataframe.loc[st.session_state.token_num][a+8]!=None})
        
    print('1',st.session_state.token_num)
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

    st.write(st.session_state.token_num)
    print('2',st.session_state.token_num)

    col0, col1, col2, col3, col4= st.columns(5)
    with col0:
        # st.subheader(f'#{data_dataframe.loc[0][1]}')
        st.session_state.button0=st.button(label=f'#0',on_click=change_counter,args=(0,))
        st.image(data_dataframe.loc[0][6])
        st.caption(f"가격 : {token_price[0]} ETH")
        print('3',st.session_state.token_num)
        # response = requests.get(data_dataframe.loc[0][6])
        # response = requests.get(data_dataframe.loc[0][6])
        # img = Image.open(BytesIO(response.content))
        # st.button(f'{st.image(image=img,output_format="PNG")}')
        # st.button(f'{st.image(data_dataframe.loc[0][6],clamp=False,output_format="PNG")}')
        
    with col1:
        # st.subheader(f'#{data_dataframe.loc[1][1]}')
        st.session_state.button1=st.button(label=f'#1',on_click=change_counter,args=(1,))
        st.image(data_dataframe.loc[1][6])
        st.caption(f"가격 : {token_price[1]} ETH")
        print('4',st.session_state.token_num)

    with col2:
        # st.subheader(f'#{data_dataframe.loc[2][1]}')
        st.session_state.button2=st.button(label=f'#2',on_click=change_counter,args=(2,))
        st.image(data_dataframe.loc[2][6])
        st.caption(f"가격 : {token_price[2]} ETH")
        print('5',st.session_state.token_num)

    with col3:
        # st.subheader(f'#{data_dataframe.loc[3][1]}')
        st.session_state.button3=st.button(label=f'#3',on_click=change_counter,args=(3,))
        st.image(data_dataframe.loc[3][6])
        st.caption(f"가격 : {token_price[3]} ETH")

    with col4:
        # st.subheader(f'#{data_dataframe.loc[4][1]}')
        st.session_state.button4=st.button(label=f'#4',on_click=change_counter,args=(4,))
        st.image(data_dataframe.loc[4][6])
        st.caption(f"가격 : {token_price[4]} ETH")

    col5, col6, col7, col8, col9= st.columns(5)
    with col5:
        # st.subheader(f'#{data_dataframe.loc[5][1]}')
        st.session_state.button5=st.button(label=f'#5',on_click=change_counter,args=(5,))
        st.image(data_dataframe.loc[5][6])
        st.caption(f"가격 : {token_price[5]} ETH")

    with col6:
        # st.subheader(f'#{data_dataframe.loc[6][1]}')
        st.session_state.button6=st.button(label=f'#6',on_click=change_counter,args=(6,))
        st.image(data_dataframe.loc[6][6])
        st.caption(f"가격 : {token_price[6]} ETH")

    with col7:
        # st.subheader(f'#{data_dataframe.loc[7][1]}')
        st.session_state.button7=st.button(label=f'#7',on_click=change_counter,args=(7,))
        st.image(data_dataframe.loc[7][6])
        st.caption(f"가격 : {token_price[7]} ETH")

    with col8:
        # st.subheader(f'#{data_dataframe.loc[8][1]}')
        st.session_state.button8=st.button(label=f'#8',on_click=change_counter,args=(8,))
        st.image(data_dataframe.loc[8][6])
        st.caption(f"가격 : {token_price[8]} ETH")

    with col9:
        # st.subheader(f'#{data_dataframe.loc[9][1]}')
        st.session_state.button9=st.button(label=f'#9',on_click=change_counter,args=(9,))
        st.image(data_dataframe.loc[9][6])
        st.caption(f"가격 : {token_price[9]} ETH")







if NFT_name == 'Azuki':
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