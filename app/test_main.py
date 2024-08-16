import pytest
from fastapi.testclient import TestClient
import sqlmodel as sql

from .main import app, get_session

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "hello world!"}

# url = "sqlite:///testing.db" # disk memory
url = "sqlite://" # in-memory
connect_args = {
    "check_same_thread": False
}

@pytest.fixture(name="session")
def session_fixture():
    engine = sql.create_engine(
        url, connect_args=connect_args, poolclass=sql.pool.StaticPool
    )
    sql.SQLModel.metadata.create_all(engine)
    with sql.Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: sql.Session):
    def get_session_override():
        return session 

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client 
    app.dependency_overrides.clear()


def test_create_hero(client: TestClient):
    response = client.post(
        "/heroes/",
        json = {
            "name": "Deadpond",
            "secret_name": "Dive Wilson"
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] is not None 
    assert data["age"] is not None 
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"

def test_create_hero_incomplete(client: TestClient):
    response = client.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == 422

def test_create_hero_invalid(client: TestClient):
    response = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {
                "message": "Do you wanna know my secret identity?"
            }
        }
    )
    assert response.status_code == 422


# to be continued ...... Why Two Fixtures.

