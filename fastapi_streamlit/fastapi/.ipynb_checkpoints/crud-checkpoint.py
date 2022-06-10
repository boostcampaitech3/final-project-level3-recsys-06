from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import List
import models #, schemas

def get_token(db: Session, token_id: int):
    return db.query(models.OtherdeedItem.token_id,
                    models.OtherdeedItem.image_original_url,
                    models.OtherdeedItem.artifact,
                    models.OtherdeedItem.is_artifact,
                    models.OtherdeedItem.category,
                    models.OtherdeedItem.environment,
                    models.OtherdeedItem.koda_clothing,
                    models.OtherdeedItem.is_koda_clothing,
                    models.OtherdeedItem.koda_core,
                    models.OtherdeedItem.koda_eyes,
                    models.OtherdeedItem.koda_head,
                    models.OtherdeedItem.is_koda_mega,
                    models.OtherdeedItem.koda_weapon,
                    models.OtherdeedItem.is_koda_weapon,
                    models.OtherdeedItem.koda_id,
                    models.OtherdeedItem.is_koda,
                    models.OtherdeedItem.koda,
                    models.OtherdeedItem.sediment,
                    models.OtherdeedItem.eastern_resource,
                    models.OtherdeedItem.western_resource,
                    models.OtherdeedItem.southern_resource,
                    models.OtherdeedItem.northern_resource,
                    models.OtherdeedItem.easteren_resource,
                    models.OtherdeedItem.environment_tier,
                    models.OtherdeedItem.sediment_tier,
                    models.OtherdeedItem.eastern_resource_tier,
                    models.OtherdeedItem.western_resource_tier,
                    models.OtherdeedItem.southern_resource_tier,
                    models.OtherdeedItem.northern_resource_tier,
                    models.OtherdeedItem.token_id_1,
                    models.OtherdeedItem.token_id_2,
                    models.OtherdeedItem.token_id_3,
                    models.OtherdeedItem.token_id_4,
                    models.OtherdeedItem.token_id_5,
                    models.OtherdeedItem.token_id_6,
                    models.OtherdeedItem.token_id_7,
                    models.OtherdeedItem.token_id_8,
                    models.OtherdeedItem.token_id_9,
                    models.OtherdeedItem.token_id_10,
                    models.OtherdeedItem.predict_value
                    ).filter(models.OtherdeedItem.token_id == token_id).first()

def get_similarity(db: Session, token_id: list):
    return db.query(models.OtherdeedSim).filter(models.OtherdeedSim.token_id == token_id).first()

def get_tokens(db: Session, token_ids: List):
    return db.query(models.OtherdeedItem).filter(or_(models.OtherdeedItem.token_id == token_id for token_id in token_ids)).all()

def get_today(db: Session):
    return db.query(models.Today).first()

def get_top10(db: Session):
    return db.query(models.Top10.token_id).order_by(desc(models.Top10.train_time)).limit(10).all()

def get_price(db : Session,token_id: int):
    return db.query(models.OtherdeedPrice.token_id, 
                    models.OtherdeedPrice.Seller_price, 
                    models.OtherdeedPrice.Seller_price_type, 
                    models.OtherdeedPrice.Buyer_price, 
                    models.OtherdeedPrice.Buyer_price_type
                    ).filter(models.OtherdeedPrice.token_id == token_id).first()
