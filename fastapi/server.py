import io

from segmentation import get_segmentator, get_segments
from starlette.responses import Response

from fastapi import FastAPI, File
# from data import db_connect

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
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
    title="DeepLabV3 image segmentation",
    description="""Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
                           Visit this URL at port 8501 for the streamlit interface.""",
    version="0.1.0",
)

# @app.post("/segmentation")
# def get_segmentation_map(file: bytes = File(...)):
#     """Get segmentation maps from image file"""
#     segmented_image = get_segments(model, file)
#     bytes_io = io.BytesIO()
#     segmented_image.save(bytes_io, format="PNG")
#     return Response(bytes_io.getvalue(), media_type="image/png")

# @app.get("/{Token_ID}")
# def get_item_info(Token_ID: str):
#     cursor.execute(f"Select * from nftdb.ITEM where Token_ID='{Token_ID}'")
#     test = cursor.fetchall()
#     return test

# @app.post("/ssd")
# def get_item_info2(Token_ID: str):
#     cursor.execute(f"Select * from nftdb.ITEM where Token_ID = {Token_ID}")
#     test = cursor.fetchall()
#     return test

@app.post("/users")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/tokens/{token_id}")
def read_token(token_id: int, db: Session = Depends(get_db)):
    db_token = crud.get_token(db, token_id=token_id)
    if db_token is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_token

# @app.post("/users/{user_id}", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)

# TODO: ITEM 테이블 or csv를 모두 가져오기
# TODO: 검색기능 -> Token_ID가 주어지면 검색 -> 10개의 관련된 ITEM ID 
# TODO: 콜렉션 정보 가져오기.
# TODO: 특성 정보를 반환하는 것.