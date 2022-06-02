import io
from fastapi import FastAPI, File, Query
# from data import db_connect

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# model = get_segmentator()
# cursor = db_connect()

app = FastAPI(
    title="NFTeam",
    description="""Obtain semantic segmentation maps of the image in input via NFTeam implemented in PyTorch.
                           Visit this URL at port 8501 for the streamlit interface.""",
    version="0.1.0",
)

@app.get("/Today/")
def read_today(db: Session = Depends(get_db)):
    db_token = crud.get_today(db)
    if db_token is None:
        raise HTTPException(status_code=404, detail="User not found")
    ret = []
    temp = ['token_id_1', 'token_id_2', 'token_id_3', 'token_id_4', 'token_id_5', 'token_id_6', 'token_id_7', 'token_id_8', 'token_id_9', 'token_id_10']
    for token in db_token.__dict__:
        if token in temp:
            ret.append(db_token.__dict__[token])
    return sorted(ret)
    # return db_token

@app.get("/token/{token_id}")
def read_token(token_id: int, db: Session = Depends(get_db)):
    db_token = crud.get_token(db, token_id=token_id)
    if db_token is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_token

@app.get("/tokens/")
def read_tokens(token_ids: List[int] = Query(None), db: Session = Depends(get_db)):
    db_tokens = crud.get_tokens(db, token_ids=token_ids)
    if db_tokens is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_tokens

@app.get("/similarities/{token_id}")
def read_token_with_similarities(token_id:  int, db: Session = Depends(get_db)):
    db_tokens = crud.get_similarity(db, token_id=token_id)
    print(db_tokens.__dict__['token_id'])
        
    if db_tokens is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_tokens.__dict__['token_id'], db_tokens.__dict__['token_id_1']
    # return db_tokens

# TODO: ITEM 테이블 or csv를 모두 가져오기
# TODO: 검색기능 -> Token_ID가 주어지면 검색 -> 10개의 관련된 ITEM ID 
# TODO: 콜렉션 정보 가져오기.
# TODO: 특성 정보를 반환하는 것.