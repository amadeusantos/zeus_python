import uuid

from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = fields.CharField(max_length=256)
    email = fields.CharField(max_length=256, unique=True, index=True)
    password = fields.TextField()
    active = fields.BooleanField(default=True, index=True)
    is_admin = fields.BooleanField(default=False, index=True)
    roles = fields.ManyToManyField(
        "models.Role", related_name="users", through="user_roles", forward_key="roles_id"
    )
    class Meta:
        table = "users"


class Role(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=128, unique=True, index=True)
    description = fields.TextField(null=True)
    active = fields.BooleanField(default=True, index=True)

    class Meta:
        table = "roles"