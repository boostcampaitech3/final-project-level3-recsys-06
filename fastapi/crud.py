from sqlalchemy.orm import Session

import models #, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.temp).filter(models.temp.id == user_id).first()

def get_token(db: Session, token_id: int):
    return db.query(models.Item).filter(models.Item.token_id == token_id).first()



