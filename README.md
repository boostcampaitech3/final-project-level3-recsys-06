# 🍃 Airflow
> <p align="center"><img src="https://user-images.githubusercontent.com/58590260/172518494-d50c7898-24c3-4b5e-93af-346ba018d634.png" width=250><br>
> Airflow을 사용하여 데이터 수집, 전처리, 훈련, 예측 작업을 연결합니다<br>
> 1시간 마다 작업을 반복합니다</p>
## 0️⃣ 워크플로우
```pyhton
input_opensea_trade_step >> input_looksrare_trade_step >> input_x2y2_trade_step >> preprocessing_step >> train_step >> predict_step >> rec10_step
```
## 1️⃣ 거래 내역 수집
- opensea, looksrare, x2y2 사이트에서 거래 내역을 selenium을 통해 가져옵니다.
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
## 2️⃣ 전처리
- 수집한 데이터를 전처리합니다.
```python
preprocessing_step = PythonOperator(
    task_id="nft_preprocessing",
    python_callable=item_preprocessing
)
```

## 3️⃣ 모델 훈련
- 전처리한 데이터로 모델 훈련을 합니다.
```python
train_step = PythonOperator(
    task_id="nft_model_train",
    python_callable=train
)
```

## 4️⃣ 예측
- NFT 아이템들의 가격을 예측합니다.
```python
 predict_step = PythonOperator(
    task_id="nft_model_predict",
    python_callable=predict
)
```
## 5️⃣ 추천
- 저평가된 NFT 아이템 10개를 뽑습니다.
```python
rec10_step = PythonOperator(
    task_id="nft_rec10",
    python_callable=rec_10_nft
)
```

