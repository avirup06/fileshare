from fastapi.testclient import TestClient
from .test_setup import client
from fileshare.common.auth.jwt_token import JWTBearer

BEARER_TOKEN = None

first_name = "user2_first_name"
last_name = "user2_last_name"
username = "user2_username"
password = "user2_password_123"


def get_token():
    global BEARER_TOKEN
    # response = client.post(
    #     "/login",
    #     json={
    #         "username": username,
    #         "password": password
    #     },
    # )
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
    data = response.json()
    BEARER_TOKEN = data["body"]["result"]["token"]

# class OverrideJWTBearer(JWTBearer):
#     async def __call__(self):
#         return True

# app.dependency_overrides[JWTBearer] = OverrideJWTBearer
# client = TestClient(app)

def get_headers(token=None, content_type = False):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': '*/*',
    }
    if content_type:
        headers["Content-Type"] = "multipart/form-data"
    return headers


def test_file_upload():
    get_token()
    with open('tests/sample_test_file.png', "wb") as f:
        response = client.post(
            "/files/upload",
            params={
                "expiry_date": "2024-06-25"
            },
            files={'file': ('sample_test_file.png', f, "image/jpeg")},
            headers=get_headers(BEARER_TOKEN, content_type=True)
        )
    assert response.status_code == 201
