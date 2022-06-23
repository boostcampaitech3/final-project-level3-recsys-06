 

# 💜 NFT 가격 예측 및 저평가된 NFT 추천
## ❗ 주제 설명
> <p align="center">
> <img src="https://user-images.githubusercontent.com/58590260/172523159-8ae4c1c3-0b85-450b-93a3-9823813ee151.png" width=500><br>
> NFT의 많은 관심에 비해 NFT를 처음 접한 사용자들은 여전히 NFT의 가격이 적절한 지 판단하기 어렵습니다.<br>
 > 이 프로젝트에서는 <b>1시간마다 거래 데이터를 수집하여 NFT 특성 데이터와 함께 모델을 훈련</b>하고<br>
> 사용자에게 <b>예측가격</b>을 제공하고 저평가 된 NFT를 추천합니다 <br>
> <b>해당 NFT와 특성이 비슷한 NFT 아이템</b>들을 사용자에게 추가 정보로 제공합니다</p>


## 👋 팀원 소개
|[강신구](https://github.com/Kang-singu)|[김혜지](https://github.com/h-y-e-j-i)|[이상연](https://github.com/qwedsazxc456)|[전인혁](https://github.com/inhyeokJeon)|
| :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------: |
|  [![Avatar](https://user-images.githubusercontent.com/58590260/163955612-1e3c1752-9c68-4cb1-af8f-c99b99625750.jpg)](https://github.com/Kang-singu) | [![Avatar](https://user-images.githubusercontent.com/58590260/163910721-c067c68a-9612-4e70-a464-a4bb84eea97e.jpg)](https://github.com/h-y-e-j-i) | [![Avatar](https://user-images.githubusercontent.com/58590260/163955925-f5609908-6984-412f-8df6-ae490517ddf4.jpg)](https://github.com/qwedsazxc456) | [![Avatar](https://user-images.githubusercontent.com/58590260/163956020-891ce159-3233-469d-a83c-4c0926ec438a.jpg)](https://github.com/inhyeokJeon) |
| Front-end,<br>Back-end | **Project Manager**, <br> Data crawling, <br> Database, <br> Airflow | EDA,<br>Data preprocessing,<br>Model | Back-end,<br>Front-end |


## 🔨 Environment
```
fastapi 0.78.0
python 3.8.5
numpy 1.19.2
pandas 1.4.2
pymysql 1.0.2
pyyaml 6.0
requests 2.27.1
torch 1.10.0
streamlit 1.9.2
selenium 4.2.0
selenium-stealth 1.0.6
```

## 📁 Directory
📁 [final-project-level3-recsys-06](https://github.com/boostcampaitech3/final-project-level3-recsys-06)\
└  📁 [DB](https://github.com/boostcampaitech3/final-project-level3-recsys-06/tree/main/DB)\
└  📁 [airflow](https://github.com/boostcampaitech3/final-project-level3-recsys-06/tree/main/airflow)\
└  📁 [fastapi_streamlit](https://github.com/boostcampaitech3/final-project-level3-recsys-06/tree/main/fastapi_streamlit)\
└  📁 [model](https://github.com/boostcampaitech3/final-project-level3-recsys-06/tree/main/model)

## 📎 Dataset
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/172515236-ec10bba1-3d09-43c0-b1ee-176778970982.png" height=150> <img src="https://user-images.githubusercontent.com/58590260/172515244-88881601-a6bb-4b2d-a617-0d668dbaa561.png" height=150> <img src="https://user-images.githubusercontent.com/58590260/172522395-7e8d984f-5c46-40da-a069-9ca7bd8ddb3e.png" height=150> <img src="https://user-images.githubusercontent.com/58590260/172522513-a31958df-77c4-40f4-87ce-5792643bd068.png" height=150>

</p>

## 🔎Data EDA
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175429269-9457593a-eeca-4457-8ea5-8d4cb294b181.png" width=700></p>

- 먼저 특성과 가격간의 관계에 대해 알아보았습니다. 각각의 특성들을 가진 NFT의 평균과 각 특성들의 유무에 따른 가격차이에 대해 확인해 보았고, NFT의 가격은 **몇몇의 특성**들에서 유의미한 차이가 존재한다는 것을 알게 되었습니다.

<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175429326-bbaa2e9a-ae4f-4465-b9f7-463b1e9baf39.png" width=700></p>

- 그 후 가격의 분포를 확인하여 **이상치를 제거**하였습니다

<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175429382-53e63a04-134f-4d24-b26f-5fbf39d1f6b0.png" width=700></p>

- NFT는 시간에 따른 가격의 변동이 심했고 가격 변동이 비슷하다고 생각되는 **일정 부분의 데이터만을 사용하여 학습** 하였습니다.

## 🏆 Model
### 💳️ 가격예측
- **선형회귀**
  - 특성들에 따른 가격 평균의 분포가 NFT 가격 분포와 비슷하였기에, 특성들의 선형 결합만으로도  NFT의 가격을 나타 낼 수 있을 것이라 판단하였습니다
  - 데이터의 수가 적어 복잡한 모델은 학습이 힘들 것이라 판단하였습니다.
- **MAPE**
  - NFT들의 가격 차이가 컸기에,
  - 실제 가격과 예측값의 차이를 퍼센트로 표현하는 것이 더 타당하다고 생각
### ♊️ 유사도
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175429639-84f48be1-95e7-412d-b982-dd7208741c95.png" width=700></p>

- **특성행렬과 전치행렬의 곱**
  - 각 특성의 유무에 따라 0과 1로 표현하였기에 이와 같은 방법으로 서로 겹치는 것의 개수를 구할 수 있었습니다
  - 자카드 유사도와 코사인 유사도 모두 이러한 방법과 분자 부분의 크기가 같고 각 NFT들의 특성의 개수가 같아 유사도의 순서는 같을 것이기에 행렬 곱 만으로 계산을 하여 유사한 NFT를 추천하였습니다.


## 📦️ Product Serving
### 🎁 서비스 아키텍처
#### 0️⃣ 전체적인 서비스 아키텍처
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/173030341-5da14d16-c05d-45a6-ab96-09ff4c121770.png" width=700></p>

- 데이터 수집 - 전처리 - 훈련 - 예측 과정은 **Airflow을 통해 1시간 간격으로 작업을 수행**합니다.
- 모든 데이터는 **Google Cloud SQL**에 저장됩니다.
- **Docker**로 FastAPI와 Streamlit 이미지를 만들고 Google Compute Engine 서버를 사용하여 배포하였습니다.
#### 1️⃣ 데이터 수집

<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175427732-e73d2011-9b23-46a8-94d3-e1fb9c38eb7d.png"></p>

- OpenSea API를 통해 **NFT 특성 데이터와 판매자가 올린 가격 및 구매를 원한 사람들의 가장 높은 제안 가격 데이터**를, Etherscan에서는 Selenium을 통해 **거래 내역 데이터**를 크롤링하여 **Google Cloude SQL**에 넣었습니다.
#### 2️⃣ 전처리 - 훈련 - 예측
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175427990-cb6a07c1-a8c5-430f-a933-b1717175fd52.png"></p>

- NFT 특성과 거래내역 데이터를 **전처리**한 후 **PyTorch 기반으로 모델을 훈련**한 뒤 **가격을 예측**합니다.. 그리고  판매자가 올린 가격 및 구매를 원한 사람들의 가장 높은 제안 가격 데이터를 비교하여 **저평가된 NFT 10개**를 구합니다.

#### 3️⃣ 유사도
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175428054-668788d7-7b1b-4032-81f2-0397b832b712.png"></p>


- **NFT 특성 데이터**를 사용하여 **해당 NFT와 비슷한 특성을 가진 10개의 NFT**을 구합니다.

#### 4️⃣ 출력

<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175428142-3e35863e-5e47-49da-9010-95f9d68cd649.png"></p>

- NFT 특성 데이터, 저평가된 10개의 NFT, NFT 예측 가격, 비슷한 특성을 가진 10개 NFT 데이터는 **FastAPI를** 통해 **Stramlit**에 출력합니다.

### 🎁 구현/데모
<p align="center"><img src="https://user-images.githubusercontent.com/58590260/175428519-de482a26-6cd2-49e7-b93a-9411fc3d1b87.png"></p>

- **저평가된 NFT 10개는** NFT Collections의 메인에 출력됩니다.
- **NFT 특성 데이터, NFT 예측 가격, 비슷한 특성을 가진 10개의 NFT 데이터**는 사용자가 보고 있는 NFT 화면에 출력됩니다.



## 🖼️ Result
- http://115.85.182.72:30001/
<p align="center"> <img src="https://user-images.githubusercontent.com/58590260/172598430-afe65f8e-2d2f-4c74-ae5e-9ada22a4fb08.png" height=200> <img src="https://user-images.githubusercontent.com/58590260/172597608-7d726934-4c24-493d-9e3c-f3d96078c31a.png" height=200> <img src="https://user-images.githubusercontent.com/58590260/172597676-e7eeb004-4cdf-45ff-bf08-5f417a81a8e8.png" height=200> </p>


## 📒 보고서
* [보고서 링크](https://thundering-astronomy-d23.notion.site/RecSys-06-Final-Project-NFT-d625dd6c789b42dea169c80c350f3454)

## 📜 참고자료
* [Airflow](https://airflow.apache.org/)
* [Etherscan](https://etherscan.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [GCP](https://cloud.google.com/)
* [Streamlit](https://streamlit.io/)
* [MySQL](https://www.mysql.com/)
* [OpenSea](https://docs.opensea.io/reference/api-overview)
* [Selenium](https://www.selenium.dev/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
