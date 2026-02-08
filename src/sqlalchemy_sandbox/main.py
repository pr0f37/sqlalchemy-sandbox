from flask import Flask, Response, request
from pydantic import ValidationError


from sqlalchemy_sandbox.db.uow import SqlUnitOfWork
from sqlalchemy_sandbox.db.models import start_mappers
from sqlalchemy_sandbox.models.user import User
from sqlalchemy_sandbox.api import marshaling

app = Flask(__name__)
start_mappers()


@app.post("/users/<db_name>")
@app.post("/users")
def create_users(db_name: str = "default"):
    try:
        request_body = marshaling.User.model_validate(request.get_json())
    except ValidationError as e:
        return Response(str(e), 400)

    u = User(**request_body.model_dump())
    with SqlUnitOfWork(db_name) as uow:
        uow.save(u)
        return marshaling.User.model_validate(u.to_dict()).model_dump()


@app.get("/users/<db_name>")
@app.get("/users")
def get_users(db_name: str = "default"):
    with SqlUnitOfWork(db_name) as uow:
        users = uow.load_all(User)
        users_list = [u.to_dict() for u in users]
    return marshaling.users.validate_python(users_list)
