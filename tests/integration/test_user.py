from fastapi.testclient import TestClient

from .test_setup import client


# client = TestClient(app)

BEARER_TOKEN = None

first_name = "user1_first_name"
last_name = "user1_last_name"
username = "user1_username"
password = "user1_password_123"



def get_headers(token):
    return {
        'Authorization': f'Bearer {token}',
        'Accept': '*/*',
    }


def test_signup():
    response = client.post(
        "/signup",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password
        },
    )
    assert response.status_code == 201


def test_login():
    global BEARER_TOKEN
    response = client.post(
        "/login",
        json={
            "username": username,
            "password": password
        },
    )
    assert response.status_code == 200
    data = response.json()
    BEARER_TOKEN = data["body"]["result"]["token"]
    print(BEARER_TOKEN)


def test_user_profile():
    global BEARER_TOKEN

    response = client.get(
        "/user/profile"
    )
    assert response.status_code == 401
    
    response = client.get(
        "/user/profile",
        headers=get_headers(BEARER_TOKEN)
    )
    assert response.status_code == 200