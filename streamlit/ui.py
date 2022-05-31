from cProfile import label
from logging import PlaceHolder
import streamlit as st
import requests

# from model import nft_dataset, linear_model, save_model, Train, get_prediction

# backend = "http://fastapi:8000/"
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
from yaml import load, FullLoader
from io import BytesIO, StringIO
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader, Dataset, random_split

def delete_none(datas: dict):
    will_be_removed = []
    for data in datas:
        if not datas[data]:
            will_be_removed.append(data)
    for i in will_be_removed:
        datas.pop(i)
    return datas

def change_counter(num): st.session_state.token_num=num

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

if st.session_state.NFT_name == 'Otherdeed for Otherside':
    if 'token_num' not in st.session_state:
        st.session_state.token_num = -1
    st.title("Otherdeed for Otherside")
    ordinal_number = ['첫', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
    st.subheader('찾고 싶은 아이템을 입력해 주세요!!!')

    select_c=st.columns((4,1))
    with select_c[0]:
        st.session_state.select_text = st.text_input(label = 'Feature name',placeholder = 'Token ID를 입력해주세요...')
        data2 = requests.get(f"http://localhost:30002/tokens/{st.session_state.select_text}").json()

    with select_c[1]:
        st.write('')
        st.write('')
        st.write('')
        st.session_state.select_button = st.button('Search')
    if st.session_state.select_button :
        if 0 <= int(st.session_state.select_text) < 100000:
            st.session_state.token_num = 10
            all_data = delete_none(data2)
            image_link = all_data.pop('image_original_url')
        else:
            st.warning('해당 Token_id가 없습니다. 다시 입력해주세요.')

    if st.session_state.token_num==10:
        st.header(f"#{st.session_state.select_text}에 대한 정보입니다.")
        st.subheader(f'추천 가격 : 0.0001 ETH')
        main_c = st.columns(2)
        with main_c[0]:
            st.image(image_link)
        with main_c[1]:
            st.write(all_data)
        back_col=st.columns(8)
        with back_col[7]:
            st.session_state.back_button=st.button('Back',on_click=change_counter,args=(-1,))


# 
# st.write(all_data)
# 
# st.image(image=image_link, caption="test")



# st.markdown("HEEELO")
# st.write(data)
# st.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://google.com.au/)")
# st.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://google.com.au/)")
# st.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://google.com.au/)")
# image_urls = ["http://www.google.com.au/images/nav_logo7.png", "http://www.google.com.au/images/nav_logo7.png", "http://www.google.com.au/images/nav_logo7.png"]
# opening_html = '<div style=display:flex;flex-wrap:wrap>'
# closing_html = '</div>'
# child_html = ['<img src="{}" style=margin:3px;width:200px;></img>'.format(url) for url in image_urls]
# gallery_html = opening_html
# for child in child_html:
#     gallery_html += child
# gallery_html += closing_html
# st.markdown(gallery_html, unsafe_allow_html=True)




# st.write({token_columns[a]:str(list(st.session_state.data_dataframe.loc[st.session_state.token_num])[a+8]) for a in range(len(token_columns)) if str(st.session_state.data_dataframe.loc[st.session_state.token_num][a+8])!='nan'})
# # data2=pd.DataFrame(data2,columns=~~~)
