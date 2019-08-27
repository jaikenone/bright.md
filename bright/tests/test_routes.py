from flask import Flask
import json

from bright.models import User, db
from bright.routes import configure_routes


def test_base_route(client):
    response = client.get("/")

    assert response.get_data() == b'Hello, world!'
    assert response.status_code == 200

def test_post_route__failure__bad_request(client):
    url = '/nothing'
    mock_request_headers = {
        'authorization-sha256': '123'
    }
    mock_request_data = {}
    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)

    assert response.status_code == 404

def test_post_route__success__user_get_all(client):
    new_user = User(
        first_name="Leto",
        last_name="Atreides",
        zip_code="11111",
        email="leto@caladan.com"
    )
    db.session.add(new_user)
    db.session.commit()

    rs = client.get("/user")

    assert rs.status_code == 200

def test_post_route__success__user_get(client):
    new_user = User(
        first_name="Leto",
        last_name="Atreides",
        zip_code="11111",
        email="leto@caladan.com"
    )
    db.session.add(new_user)
    db.session.commit()

    rs = client.get("/user/1")

    assert rs.status_code == 200

def test_post_route__success__user_create(client):
    mock_request_data = {
        "first_name": "Paul",
        "last_name": "Atreides",
        "zip_code": "11111",
        "email": "leto@caladan.com"
    }

    rs = client.post(
        "/user/create",
        content_type='application/json',
        data=json.dumps(mock_request_data)
    )

    assert rs.status_code == 200

def test_post_route__success__user_delete(client):
    new_user = User(
        first_name="Leto",
        last_name="Atreides",
        zip_code="11111",
        email="leto@caladan.com"
    )
    db.session.add(new_user)
    db.session.commit()

    rs = client.delete("/user/delete/1")

    assert rs.status_code == 200

def test_post_route__success__user_update(client):
    new_user = User(
        first_name="Leto",
        last_name="Atreides",
        zip_code="11111",
        email="leto@caladan.com"
    )
    db.session.add(new_user)
    db.session.commit()

    mock_request_data = {
        "id": 1,
        "zip_code": "11111"
    }

    rs = client.patch(
        "/user/update",
        content_type='application/json',
        data=json.dumps(mock_request_data)
    )

    assert rs.status_code == 200
