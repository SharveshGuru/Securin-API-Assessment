import json
from sqlalchemy.orm import Session
from models import Recipies

def add_recipie(db: Session,
                cuisine:str,
                title:str,
                rating:float,
                prep_time:int,
                cook_time:int,
                total_time:int,
                description: str,
                nutrients: json,
                serves:str,
                calories:int):
    recipie=Recipies(
        cuisine=cuisine,
        title=title,
        rating=rating,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        description=description,
        nutrients=nutrients,
        serves=serves,
        calories=calories
    )
    db.add(recipie)
    db.commit()
    db.refresh(recipie)
    print("Added recipie")
    return recipie
    
    