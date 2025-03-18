import uuid

from pydantic import create_model
from sqlmodel import Field, SQLModel

from ..models.dynamic_models import ID_FIELD


class PKCE(SQLModel):

    host: str = Field(
        default=None,
        unique=True,
        title="Host",
        description=(
            "The host associated with the PKCE request. Must "
            "be unique across all entries."
        ),
    )
    code_challenge: str = Field(
        default=None,
        max_length=255,
        title="Code Challenge",
        description=(
            "The code challenge used in the PKCE flow. Must "
            "be a valid string representation of the challenge."
        ),
    )
    code_challenge_method: str = Field(
        default=None,
        max_length=255,
        title="Code Challenge Method",
        description=(
            "The method used to generate the code challenge. "
            "Common methods include 'S256' for SHA-256."
        ),
    )


field_definitions = {}
field_definitions[ID_FIELD] = (
    uuid.UUID,
    Field(default_factory=uuid.uuid4, primary_key=True),
)
field_definitions["__tablename__"] = (str, "pkce")
PKCEType = create_model(
    "PKCE",
    __base__=PKCE,
    **field_definitions,
    __cls_kwargs__={"table": True},
)
