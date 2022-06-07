from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import List
import models #, schemas

def get_token(db: Session, token_id: int):
    return db.query(models.OtherdeedItem).filter(models.OtherdeedItem.token_id == token_id).first()

def get_similarity(db: Session, token_id: list):
    return db.query(models.OtherdeedSim).filter(models.OtherdeedSim.token_id == token_id).first()

def get_tokens(db: Session, token_ids: List):
    return db.query(models.OtherdeedItem).filter(or_(models.OtherdeedItem.token_id == token_id for token_id in token_ids)).all()

def get_today(db: Session):
    return db.query(models.Today).first()

def get_top10(db: Session):
    return db.query(models.Top10.token_id).order_by(desc(models.Top10.train_time)).limit(10).all()
