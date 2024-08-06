import sqlmodel as sql
from fastapi import FastAPI, HTTPException, Query

from .models import Hero, HeroCreate, HeroPublic, HeroUpdate
from .database import create_db_tables, engine

# instance of fastapi
app = FastAPI()

# hash function
def hash_password(password):
    return f"not really hashed {password} hehehe"

# create db and table at start-time
@app.on_event("startup")
def on_startup():
    create_db_tables()

# create a hero
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate):
    hashed_password = hash_password(hero.password)
    with sql.Session(engine) as session:
        extra_data = {"hashed_password": hashed_password}
        db_hero = Hero.model_validate(hero, update=extra_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

# list all heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def get_heroes():
    with sql.Session(engine) as session:
        heroes = session.exec(sql.select(Hero)).all()
        return heroes
    
# list a limited number of heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def get_limit(offset: int = 0, limit: int = Query(default=10, le=100)):
    with sql.Session(engine) as session:
        heroes = session.exec(
            sql.select(Hero).offset(offset).limit(limit).all()
        )
        return heroes

# read one hero
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def get_hero(hero_id: int):
    with sql.Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(
                status_code = 404,
                detail="Hero not found"
            )
        return hero

# update model
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate):
    extra_data = {}
    with sql.Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(
                status_code = 404,
                detail = "Hero not Found"
            )
        hero_data = hero.model_dump(exclude_unset=True)
        if "password" in hero_data:
            hashed_password = hash_password(hero_data.password)
            extra_data["hashed_password"] = hashed_password
        db_hero.sqlmodel_update(hero_data, update=extra_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with sql.Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(
                status_code = 404,
                detail="Hero not found"
            )
        session.delete(db_hero)
        session.commit()
        return {"Ok": True}
        



