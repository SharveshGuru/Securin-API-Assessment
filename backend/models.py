from sqlalchemy import Column, DateTime, Float, Text, String, Integer, JSON
from database import Base

class Recipies(Base):
    __tablename__ = 'recipies'
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    cuisine=Column(String(50), nullable=False)
    title=Column(String(100))
    rating=Column(Float)
    prep_time=Column(Integer)
    cook_time=Column(Integer)
    total_time=Column(Integer)
    description=Column(Text)
    nutrients=Column(JSON)
    serves=Column(String(50))
    
    
    