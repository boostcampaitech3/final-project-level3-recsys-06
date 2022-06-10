#  🥫 DB
> <p align="center"><img src="https://user-images.githubusercontent.com/58590260/173030107-100c3157-efce-41ae-9852-e2c465212b4f.png" width=700><br>
> Opensea는 API를 통해 NFT 특성과 판매자가 올린 가격과 가장 높은 제안 가격 데이터를, <br>
> Etherscan은 Selenium을 통해 거래 내역 데이터를 가져와 Google Cloud SQL에 저장합니다
> </p>

- **insert_itemdb.py** : NFT 특성 데이터를 MySQL 테이블에 넣는 코드
- **insert_priceofferdb.py**  : 판매자가 올린 가격과 가장 높은 제안 가격 데이터를 MySQL 테이블에 넣는 코드
- **insert_tradedb.py** : 거래 내역을  MySQL 테이블에 넣는 코드
- **selenium_server.py** : selenium을 서버에서 실행시키기 위한 테스트 코드
