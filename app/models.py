import sqlmodel as sql 

# Team

class TeamBase(sql.SQLModel):
    name: str = sql.Field(index=True)
    headquarters: str 

class Team(TeamBase, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    heroes: list["Hero"] = sql.Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass 

class TeamPublic(TeamBase):
    id: int 

class TeamUpdate(TeamBase):
    name: str|None = None
    headquarters: str|None = None 


# Hero

class HeroBase(sql.SQLModel):
    name: str = sql.Field(index=True)
    secret_name: str 
    age: int|None = sql.Field(default=None, index=True)
    team_id: int|None = sql.Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    hashed_password: str = sql.Field()
    team: Team | None = sql.Relationship(back_populates="heroes")

class HeroCreate(HeroBase):
    password: str 

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(HeroBase):
    name: str|None = None 
    secret_name: str|None = None 
    age: int|None = None
    password: str|None = None
    team_id: int|None = None


# models with relationships

class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None

class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []


