from typing import List
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from sqlalchemy import text
from database import session, engine
from models import Base, Recipies
from sqlalchemy.orm import Session
import json 
from crud import add_recipie
from fastapi.middleware.cors import CORSMiddleware
import math

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

class RecipieSchema(BaseModel):
    id:int
    cuisine:str
    title:str
    rating:float
    prep_time:int
    cook_time:int
    total_time:int
    description: str
    nutrients: dict
    serves:str
    
    class Config:
        orm_mode=True

class RecipiePaginated(BaseModel):
    total:int
    data:List[RecipieSchema]
    
@app.get("/store_recipies")
def store_recipies(db:Session=Depends(get_db)):
    with open(r'C:\stuff\Securin-API-Assessment\backend\US_recipes_null.json') as file:
        file_data = json.load(file)
        for id in file_data:
            recipie=file_data[id]
            cuisine=recipie['cuisine']
            title=recipie['title']
            rating=recipie['rating']
            prep_time=recipie['prep_time']
            cook_time=recipie['cook_time']
            total_time=recipie['total_time']
            description=recipie["description"]
            serves=recipie["serves"]
            nutrients=recipie["nutrients"]
            
            if rating is None:
                rating=-1.0
            
            if prep_time is None:
                prep_time=-1
            
            if cook_time is None:
                cook_time=-1
                
            if total_time is None:
                total_time=-1
            
            add_recipie(db,cuisine,title,rating,prep_time,cook_time,total_time,description,nutrients,serves)
    
    return {"message":"Added recipies successfully!"}

@app.get("/api/recipies",response_model=RecipiePaginated)
def get_recipies(db:Session=Depends(get_db),
                 page:int=Query(1,ge=1),
                 limit:int=Query(10,ge=1)):
    total=db.query(Recipies).count()
    total=math.ceil(total/limit)
    data= db.query(Recipies).order_by(text("rating desc")).offset((page-1)*limit).limit(limit).all()
    return {"total":total,"data":data}

