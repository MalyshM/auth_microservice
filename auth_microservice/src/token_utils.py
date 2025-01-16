import os
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()
ID_FIELD = os.getenv("ID_FIELD", "")
ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP", "15"))
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY", "do not use default!")
REFRESH_TOKEN_EXP = int(os.getenv("REFRESH_TOKEN_EXP", "30"))
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "do not use default!")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_access_token(
    data: dict, expiration_minutes: int = ACCESS_TOKEN_EXP
) -> str:
    expiration = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(minutes=expiration_minutes)
    data["exp"] = expiration
    if data[ID_FIELD]:
        data[ID_FIELD] = str(data[ID_FIELD])
    token = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(
    data: dict, expiration_days: int = REFRESH_TOKEN_EXP
) -> str:
    expiration = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(days=expiration_days)
    data["exp"] = expiration
    if data[ID_FIELD]:
        data[ID_FIELD] = str(data[ID_FIELD])
    token = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.InvalidSignatureError as e:
        raise e
    except jwt.InvalidTokenError as e:
        raise e


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.InvalidSignatureError as e:
        raise e
    except jwt.InvalidTokenError as e:
        raise e


def refresh_access_token(refresh_token: str) -> str:
    payload = verify_refresh_token(refresh_token)
    new_access_token = create_access_token(data=payload)
    return new_access_token


# Example usage
if __name__ == "__main__":
    # User data to encode in the tokens
    user_data = {"user_id": 123, "username": "example_user"}

    # Create tokens
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    print(f"Generated Access Token: {access_token}")
    print(f"Generated Refresh Token: {refresh_token}")

    # Verify tokens
    try:
        decoded_access_payload = verify_access_token(access_token)
        print(f"Decoded Access Payload: {decoded_access_payload}")
    except Exception as e:
        print(f"Error verifying access token: {e}")

    try:
        decoded_refresh_payload = verify_refresh_token(refresh_token)
        print(f"Decoded Refresh Payload: {decoded_refresh_payload}")
    except Exception as e:
        print(f"Error verifying refresh token: {e}")

    # Refresh the access token
    try:
        new_access_token = refresh_access_token(refresh_token)
        print(f"New Access Token: {new_access_token}")
    except Exception as e:
        print(f"Error refreshing access token: {e}")

    decoded_access_payload = verify_access_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZV91c2VyIiwiZXhwIjoxNzM1MzgzNzg3fQ.UZ7X5dxTXCL-z0x8PQOl5nCAwUaN18Ws2IIq21Ja-mU"
    )
    print(f"Decoded Access Payload: {decoded_access_payload}")