from typing import List, Optional

from pydantic import BaseModel, BaseSettings, SecretStr
import streamlit as st

# Slide 3: Basic Model

class User(BaseModel):
    id: int
    name: str = "Jane Doe"

data = {"id": 19, "name": "Fanilo", "age": 179}
user = User(**data)
st.write(user)

data = {"id": "Fanilo", "name": 42}
user = User(**data)
#st.write(user)

# Slide 4: Hierarchical Model

class Address(BaseModel):
    city: str
    street: Optional[str]


class User(BaseModel):
    id: int
    name: str
    addresses: List[Address]


data = {
    "id": 42,
    "name": "Fanilo",
    "addresses": [{"city": "Paris"}, {"city": "Tokyo", "street": "こんにちは"}],
}
user = User(**data)
st.success(user.addresses[1].street)

# Slide 7: Secrets

class Settings(BaseSettings):
    auth_key: SecretStr
    api_key: str

    class Config:
        env_file = "settings.env"

st.write(Settings().dict())
