from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Top10(Base):
    __tablename__ = "TOP_10_ITEMS"
    # image_preview_url, image_thumbnail_url, image_original_url, external_link, artifact, is_artifact, category, eastern_resource, environment, koda_clothing, is_koda_clothing, koda_core, koda_eyes, koda_head, is_koda_mega, koda_weapon, is_koda_weapon, koda_id, is_koda, northern_resource, sediment, southern_resource, western_resource, easteren_resource, environment_tier, koda, northern_resource_tier, plot, sediment_tier, southern_resource_tier, western_resource_tier, eastern_resource_tier
    token_id = Column(Integer, primary_key=True)
    train_time = Column(DateTime)

class Today(Base):
    __tablename__ = "temp_today"
    # image_preview_url, image_thumbnail_url, image_original_url, external_link, artifact, is_artifact, category, eastern_resource, environment, koda_clothing, is_koda_clothing, koda_core, koda_eyes, koda_head, is_koda_mega, koda_weapon, is_koda_weapon, koda_id, is_koda, northern_resource, sediment, southern_resource, western_resource, easteren_resource, environment_tier, koda, northern_resource_tier, plot, sediment_tier, southern_resource_tier, western_resource_tier, eastern_resource_tier
    date = Column(String, primary_key=True)
    token_id_1 = Column(Integer)
    token_id_2 = Column(Integer)
    token_id_3 = Column(Integer)
    token_id_4 = Column(Integer)
    token_id_5 = Column(Integer)
    token_id_6 = Column(Integer)
    token_id_7 = Column(Integer)
    token_id_8 = Column(Integer)
    token_id_9 = Column(Integer)
    token_id_10 = Column(Integer)

class OtherdeedItem(Base):
    __tablename__ = "ITEM"
    #id = Column(Integer)
    token_id = Column(Integer, primary_key=True)
    # asset_contract_address =Column(String, primary_key=True)
    #image_url = Column(String)
    # image_preview_url = Column(String)
    # image_thumbnail_url = Column(String)
    image_original_url = Column(String)
    # external_link = Column(String)
    artifact = Column(String)
    is_artifact = Column(String)
    category = Column(String)
    eastern_resource = Column(String)
    environment = Column(String)
    koda_clothing = Column(String)
    is_koda_clothing = Column(String)
    koda_core = Column(String)
    koda_eyes = Column(String)
    koda_head = Column(String)
    is_koda_mega = Column(String)
    koda_weapon = Column(String)
    is_koda_weapon = Column(String)
    koda_id = Column(String)
    is_koda = Column(String)
    northern_resource = Column(String)
    sediment = Column(String)
    southern_resource = Column(String)
    western_resource = Column(String)
    easteren_resource = Column(String)
    environment_tier = Column(String)
    koda = Column(String)
    northern_resource_tier = Column(String)
    #plot = Column(String)
    sediment_tier = Column(String)
    southern_resource_tier = Column(String)
    western_resource_tier = Column(String)
    eastern_resource_tier = Column(String)
    token_id_1 = Column(Integer)
    token_id_2 = Column(Integer)
    token_id_3 = Column(Integer)
    token_id_4 = Column(Integer)
    token_id_5 = Column(Integer)
    token_id_6 = Column(Integer)
    token_id_7 = Column(Integer)
    token_id_8 = Column(Integer)
    token_id_9 = Column(Integer)
    token_id_10 = Column(Integer)
    predict_value = Column(Float)

class OtherdeedSim(Base):
    __tablename__ = "SIMILARITY_ITEMS"
    #id = Column(Integer)
    token_id = Column(Integer, primary_key=True)
    token_id_1 = Column(Integer)
    token_id_2 = Column(Integer)
    token_id_3 = Column(Integer)
    token_id_4 = Column(Integer)
    token_id_5 = Column(Integer)
    token_id_6 = Column(Integer)
    token_id_7 = Column(Integer)
    token_id_8 = Column(Integer)
    token_id_9 = Column(Integer)
    token_id_10 = Column(Integer)
