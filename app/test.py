from fastapi.testclient import TestClient
from .app import main

client = TestClient(main.App, raise_server_exceptions=False)


def test_welcome():

    resp = client.get("/")
    assert resp.status_code == 200

    message = "Welcome!"
    assert resp.json() == message

def test_device_add():

    data = {
        "id": 0,
        "name": "NextSeq 550",
        "country": "USA"
    }
    resp = client.put("/device_add", data=data)
    assert resp.status_code == 500


def test_article_add():
   
    data = {
        "id": 3,
        "title": "Inferring pattern-driving intercellular flows from single-cell and spatial transcriptomics",
    }
    resp = client.put("/article_add", data=data)
    assert resp.status_code == 500

def test_application_add():
   
    data = {
        "record_id": 1,
        "device_id": 0,
        "article_id": 3,
        "seq_obj": "tumor, RNA",
    }
    resp = client.put("/application_add", data=data)
    assert resp.status_code == 500


def test_device_get():
  
    resp1 = client.get("/device?id=1")
    assert resp1.status_code == 200
    answer1 = {
        "id": 0,
        "name": "NextSeq 550",
        "country": "USA"
    }
    assert resp1.json() == answer1

    resp2 = client.get("/device?id=abracadabra")
    assert resp2.status_code == 422


def test_article_get():
  
    resp1 = client.get("/article?id=2")
    assert resp1.status_code == 200
    assert resp1.json () == {
        "id": "3",
        "title": "Inferring pattern-driving intercellular flows from single-cell and spatial transcriptomics"
    }

    resp2 = client.get("/article?id=abracadabra")
    assert resp2.status_code == 422


def test_application_get():
  
    resp1 = client.get("/application?record_id=0")
    assert resp1.status_code == 200
    assert resp1.json () == {
        "record_id": 1,
        "device_id": 0,
        "article_id": 3,
        "seq_obj": "tumor, RNA"
    }

    resp2 = client.get("/application?record_id=abracadabra")
    assert resp2.status_code == 422
