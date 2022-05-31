from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class temp(Base):
    __tablename__ = "temp"
    id = Column(Integer, primary_key=True)
    password =  Column(String) 
    # image_preview_url, image_thumbnail_url, image_original_url, external_link, artifact, is_artifact, category, eastern_resource, environment, koda_clothing, is_koda_clothing, koda_core, koda_eyes, koda_head, is_koda_mega, koda_weapon, is_koda_weapon, koda_id, is_koda, northern_resource, sediment, southern_resource, western_resource, easteren_resource, environment_tier, koda, northern_resource_tier, plot, sediment_tier, southern_resource_tier, western_resource_tier, eastern_resource_tier


class Item(Base):
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