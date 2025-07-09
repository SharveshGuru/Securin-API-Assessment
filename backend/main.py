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
from pydantic import SkipValidation
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
    nutrients: SkipValidation[dict]
    serves:str
    calories:int
    
    class Config:
        orm_mode=True

class RecipiePaginated(BaseModel):
    total:int
    page:int
    limit:int
    data:List[RecipieSchema]

class RecipieList(BaseModel):
    total:List[RecipieSchema]
    
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
            calories=-1
            try:
                calories_string=nutrients["calories"]
                value,unit=map(str,calories_string.split(" "))
                calories=int(value)
            except:
                calories_string=""
                
            if rating is None:
                rating=-1.0
            
            if prep_time is None:
                prep_time=-1
            
            if cook_time is None:
                cook_time=-1
                
            if total_time is None:
                total_time=-1
                
            if serves is None:
                serves=""
            
            if title is None:
                title=""
            
            if description is None:
                description=""
            
            add_recipie(db,cuisine,title,rating,prep_time,cook_time,total_time,description,nutrients,serves,calories)
    
    return {"message":"Added recipies successfully!"}

@app.get("/api/recipies",response_model=RecipiePaginated)
def get_recipies(db:Session=Depends(get_db),
                 page:int=Query(1,ge=1),
                 limit:int=Query(10,ge=1)):
    total=db.query(Recipies).count()
    total=math.ceil(total/limit)
    data= db.query(Recipies).order_by(text("rating desc")).offset((page-1)*limit).limit(limit).all()
    return {"total":total,"page":page,"limit":limit,"data":data}

@app.get("/api/recipies/search",response_model=RecipieList)
def search_recipies(db:Session=Depends(get_db),
                    maxCalories:int | None=None,
                    minCalories:int | None=None,
                    calories:int | None=None,
                    maxTotalTime: int | None=None,
                    minTotalTime: int | None=None,
                    totalTime: int | None=None,
                    maxRating:float | None=None,
                    minRating:float | None=None,
                    rating:float | None=None,
                    cuisine:str | None=None,
                    title:str | None=None
                    ):
    
    data=db.query(Recipies).order_by(text("rating desc"))
    
    if maxCalories:
        data=data.filter(Recipies.calories!=None).filter(Recipies.calories<=maxCalories)
    
    if minCalories:
        data=data.filter(Recipies.calories>=minCalories)
        
    if calories:
        data=data.filter(Recipies.calories==calories)
    
    if maxTotalTime:
        data=data.filter(Recipies.total_time<=totalTime)
    
    if minTotalTime:
        data=data.filter(Recipies.total_time>=minTotalTime)
        
    if totalTime:
        data=data.filter(Recipies.total_time==totalTime)
        
    if maxRating:
        data=data.filter(Recipies.rating<=maxRating)
    
    if minRating:
        data=data.filter(Recipies.rating>=minRating)
        
    if rating:
        data=data.filter(Recipies.rating==rating)
        
    if cuisine:
        data=data.filter(Recipies.cuisine==cuisine)
        
    if title:
        data=data.filter(Recipies.title.ilike(f"%{title}%"))
        
    return {"total": data.all()}