import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Union

import jwt
from fastapi import FastAPI
from pydantic import BaseModel

user_to_roles = {
    "Fanilo": ["admin", "editor", "viewer"],
    "Jenny": ["editor", "viewer"],
    "John": ["viewer"],
}

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
        }
    )
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/token/{username}")
async def login_for_access_token(username: str) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": username,
            "roles": user_to_roles.get(username, []),
        },
        expires_delta=access_token_expires,
    )
    time.sleep(4)
    return Token(access_token=access_token, token_type="bearer")
