#  🥫 DB
> <p align="center"><img src="https://user-images.githubusercontent.com/58590260/172516966-f1be43c0-1425-48bf-9334-fa1d36974134.png" width=400></p><br>
> Opensea는 API를 통해 NFT 특성과 판매자가 올린 가격과 가장 높은 제안 가격 데이터를, Etherscan은 Selenium을 통해 거래 내역 데이터를 가져와 MySQL DB에 넣습니다
- **insert_itemdb.py** : NFT 특성 데이터를 MySQL 테이블에 넣는 코드\
- **insert_priceofferdb.py**  : 판매자가 올린 가격과 가장 높은 제안 가격 데이터를 MySQL 테이블에 넣는 코드\
- **insert_tradedb.py** : 거래 내역을  MySQL 테이블에 넣는 코드\
- **selenium_server.py** : selenium을 서버에서 실행시키기 위한 테스트 코드\
