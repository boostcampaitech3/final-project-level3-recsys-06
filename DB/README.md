#  ๐ฅซ DB
> <p align="center"><img src="https://user-images.githubusercontent.com/58590260/173030107-100c3157-efce-41ae-9852-e2c465212b4f.png" width=700><br>
> Opensea๋ API๋ฅผ ํตํด NFT ํน์ฑ๊ณผ ํ๋งค์๊ฐ ์ฌ๋ฆฐ ๊ฐ๊ฒฉ๊ณผ ๊ฐ์ฅ ๋์ ์ ์ ๊ฐ๊ฒฉ ๋ฐ์ดํฐ๋ฅผ, <br>
> Etherscan์ Selenium์ ํตํด ๊ฑฐ๋ ๋ด์ญ ๋ฐ์ดํฐ๋ฅผ ๊ฐ์ ธ์ Google Cloud SQL์ ์ ์ฅํฉ๋๋ค
> </p>

- **insert_itemdb.py** : NFT ํน์ฑ ๋ฐ์ดํฐ๋ฅผ MySQL ํ์ด๋ธ์ ๋ฃ๋ ์ฝ๋
- **insert_priceofferdb.py**  : ํ๋งค์๊ฐ ์ฌ๋ฆฐ ๊ฐ๊ฒฉ๊ณผ ๊ฐ์ฅ ๋์ ์ ์ ๊ฐ๊ฒฉ ๋ฐ์ดํฐ๋ฅผ MySQL ํ์ด๋ธ์ ๋ฃ๋ ์ฝ๋
- **insert_tradedb.py** : ๊ฑฐ๋ ๋ด์ญ์  MySQL ํ์ด๋ธ์ ๋ฃ๋ ์ฝ๋
- **selenium_server.py** : selenium์ ์๋ฒ์์ ์คํ์ํค๊ธฐ ์ํ ํ์คํธ ์ฝ๋
