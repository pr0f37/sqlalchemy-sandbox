from pydantic import BaseModel, TypeAdapter
from sqlalchemy_sandbox.models import user


class User(BaseModel, user.User):
    pass


users = TypeAdapter(list[User])
