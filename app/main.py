import sqlmodel as sql
from fastapi import FastAPI, Depends, Query, HTTPException

from .database import create_db_tables, engine
from .models import Hero, HeroCreate, HeroPublic, HeroUpdate, Team, TeamPublic, TeamPublicWithHeroes, HeroPublicWithTeam

# create an instance of fastapi
app = FastAPI()


# on startup of the app
@app.on_event("startup")
def on_startup():
    create_db_tables()

# setup session
def get_session():
    with sql.Session(engine) as session:
        yield session 

# get one hero
@app.get("heroes/{hero_id}", response_model=HeroPublicWithTeam)
def get_hero(*, hero_id: int, session: sql.Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )
    return hero

# get some heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    *,
    session: sql.Session = Depends(get_session),
    offset: int = 0, 
    limit: int = Query(default=100, le=100)
    ):
    heroes= session.exec(sql.select(Hero)).offset(offset).limit(limit).all()
    return heroes

# get all heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def get_all_heroes(*, session: sql.Session = Depends(get_session)):
    heroes = session.exec(sql.select(Hero)).all()
    return heroes

def hash_password(password: str) -> str:
    return f"not really hashed{password} hehe"

# create a hero
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(*, session: sql.Session = Depends(get_session), hero: HeroCreate
    ):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
    # hashed_password = hash_password(hero.password)
    # with sql.Session(engine) as session:
    #     extra_data = {"hashed_password": hashed_password}
    #     db_hero = Hero.model_validate(hero, update=extra_data)
    #     session.add(db_hero)
    #     session.commit()
    #     session.refresh(hero)
    #     return hero
    
# update hero
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(*, hero_id: int, session: sql.Session = Depends(get_session), hero: HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(
            status_code=404,
            detail="Hero not found"
        )
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        password = hero_data["password"]
        hashed_password = hash_password(password)
        extra_data["hashed_password"] = hashed_password
    db_hero.sqlmodel_update(hero_data, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: sql.Session = Depends(get_session), hero_id: int) -> dict:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(
            status_code = 404, 
            detail = "Hero not found."
        )
    session.delete(db_hero)
    session.commit()
    return {"ok": True}

# Team routes

# read a team
@app.get("/teams/{team_id}", response_model=TeamPublicWithHeroes)
def read_team(*, team_id: int, session: sql.Session = Depends(get_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )
    return db_team





