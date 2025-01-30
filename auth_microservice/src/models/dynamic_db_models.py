import uuid

from pydantic import create_model, model_validator
from .dynamic_models import (
    ID_FIELD,
    TABLE_NAME,
    validate_from_db,
    UserCreateType,
)
from sqlmodel import Field

field_definitions = {}
validators = {}
field_definitions[ID_FIELD] = (
    uuid.UUID,
    Field(default_factory=uuid.uuid4, primary_key=True),
)
field_definitions["__tablename__"] = (str, TABLE_NAME)
# UserType = create_model(
#     "User",
#     __base__=UserCreateType,
#     __validators__=validators,
#     **field_definitions,
#     __cls_kwargs__={"table": True},
# )
validators["validate"] = model_validator(mode="before")(validate_from_db)

UserDBType = create_model(
    "User",
    __base__=UserCreateType,
    __validators__=validators,
    **field_definitions,
    __cls_kwargs__={"table": True},
)
