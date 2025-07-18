from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.core.config import settings

Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(255), index=True)
    about_text = Column(Text)
    contacts = Column(JSON)
    social_handles = Column(JSON)
    policies = Column(JSON)
    faqs = Column(JSON)
    important_links = Column(JSON)
    hero_products = Column(JSON)
    full_product_catalog = Column(JSON)
    competitors = relationship("Competitor", back_populates="brand")

class Competitor(Base):
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    competitor_brand_name = Column(String(255), index=True)
    about_text = Column(Text)
    contacts = Column(JSON)
    social_handles = Column(JSON)
    policies = Column(JSON)
    faqs = Column(JSON)
    important_links = Column(JSON)
    hero_products = Column(JSON)
    full_product_catalog = Column(JSON)
    brand = relationship("Brand", back_populates="competitors")

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)
