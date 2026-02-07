from sqlalchemy import Table, Column, String, UUID
from sqlalchemy.orm import registry
from sqlalchemy_sandbox.models.user import User
import uuid

mapper_registry = registry()
user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)


def start_mappers():
    mapper_registry.map_imperatively(User, user_table)
    return mapper_registry.metadata
