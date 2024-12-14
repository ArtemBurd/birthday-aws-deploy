import pytest
from server import app, days_until_birthday
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert b'The light inside has broken but i still work' in response.data
    
def test_get_next_bday(client):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    
    response1 = client.post("/when", json={"birthday": str(today)})
    assert response1.status_code == 200
    assert response1.json["Days until next birthday"] == 0
    
    date2 = today + timedelta(days=1)
    response2 = client.post("/when", json={"birthday": str(date2)})
    assert response2.status_code == 200
    assert response2.json["Days until next birthday"] == 1
    
    date3 = today + timedelta(days=364)
    response3 = client.post("/when", json={"birthday": str(date3)})
    assert response3.status_code == 200
    assert response3.json["Days until next birthday"] == 364
    