# ๐ Airflow
> <p align="center"><img src="https://user-images.githubusercontent.com/58590260/172881187-dd018415-044a-4e80-8ff7-0c2a73dd7570.png" height=200><br>
> Airflow์ ์ฌ์ฉํ์ฌ ๋ฐ์ดํฐ ์์ง, ์ ์ฒ๋ฆฌ, ํ๋ จ, ์์ธก ์์์ ์ฐ๊ฒฐํฉ๋๋ค<br>
> 1์๊ฐ ๋ง๋ค ์์์ ๋ฐ๋ณตํฉ๋๋ค</p>
## 0๏ธโฃ ์ํฌํ๋ก์ฐ
```pyhton
input_opensea_trade_step >> input_looksrare_trade_step >> input_x2y2_trade_step >> preprocessing_step >> train_step >> predict_step >> rec10_step
```
## 1๏ธโฃ ๊ฑฐ๋ ๋ด์ญ ์์ง
- opensea, looksrare, x2y2 ์ฌ์ดํธ์์ ๊ฑฐ๋ ๋ด์ญ์ selenium์ ํตํด ๊ฐ์ ธ์ต๋๋ค.
```python
input_opensea_trade_step = PythonOperator(
        task_id="nft_input_opensea_trade",
        python_callable=input_opensea_trade_data
    )

    input_looksrare_trade_step = PythonOperator(
        task_id="nft_input_looksrare_trade",
        python_callable=input_looksrare_trade_data
    )

    input_x2y2_trade_step = PythonOperator(
        task_id="nft_input_x2y2_trade",
        python_callable=input_x2y2_trade_data
    )
```
## 2๏ธโฃ ์ ์ฒ๋ฆฌ
- ์์งํ ๋ฐ์ดํฐ๋ฅผ ์ ์ฒ๋ฆฌํฉ๋๋ค.
```python
preprocessing_step = PythonOperator(
    task_id="nft_preprocessing",
    python_callable=item_preprocessing
)
```

## 3๏ธโฃ ๋ชจ๋ธ ํ๋ จ
- ์ ์ฒ๋ฆฌํ ๋ฐ์ดํฐ๋ก ๋ชจ๋ธ ํ๋ จ์ ํฉ๋๋ค.
```python
train_step = PythonOperator(
    task_id="nft_model_train",
    python_callable=train
)
```

## 4๏ธโฃ ์์ธก
- NFT ์์ดํ๋ค์ ๊ฐ๊ฒฉ์ ์์ธกํฉ๋๋ค.
```python
 predict_step = PythonOperator(
    task_id="nft_model_predict",
    python_callable=predict
)
```
## 5๏ธโฃ ์ถ์ฒ
- ์ ํ๊ฐ๋ NFT ์์ดํ 10๊ฐ๋ฅผ ๋ฝ์ต๋๋ค.
```python
rec10_step = PythonOperator(
    task_id="nft_rec10",
    python_callable=rec_10_nft
)
```

