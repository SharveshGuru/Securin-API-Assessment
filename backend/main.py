from fastapi import FastAPI, Depends
from sqlalchemy import JSON
from database import session, engine
from models import Base, Recipies
from sqlalchemy.orm import Session
import json 
from crud import add_recipie

app=FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
        
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
            nutrients=json.dumps(recipie["nutrients"])
            
            add_recipie(db,cuisine,title,rating,prep_time,cook_time,total_time,description,nutrients,serves)
    
    return {"message":"Added recipies successfully!"}
            
            
            
        
        
    
    
