import sqlmodel as sql
from typing import Optional


class HeroBase(sql.SQLModel):
    name: str = sql.Field(index=True)
    secret_name: str
    age: int|None = sql.Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    hashed_password: str = sql.Field()

class HeroCreate(HeroBase):
    hashed_password: str

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(sql.SQLModel):
    name: str|None = None 
    secret_name: str|None = None
    age: int|None = None
    hashed_password: str|None = None







