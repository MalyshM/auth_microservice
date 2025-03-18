from typing import Optional

from pydantic import BaseModel, Field, model_validator


class PKCE_scheme(BaseModel):

    code_verifier: Optional[str] = Field(
        default=None,
        title="Code Verifier",
        description=(
            "A string that serves as the code verifier. "
            "It is used to ensure that the authorization "
            "code was not intercepted."
        ),
    )
    code_challenge: Optional[str] = Field(
        default=None,
        title="Code Challenge",
        description=(
            "A string that represents the code challenge. "
            "It is derived from the code verifier and is "
            "sent to the authorization server."
        ),
    )
    code_challenge_method: Optional[str] = Field(
        default=None,
        title="Code Challenge Method",
        description=(
            "A string indicating the method used to generate "
            "the code challenge. "
            "Common methods include 'plain' and 'S256' for SHA-256."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def pkce_validate(cls, dict_values: dict) -> dict:

        if (
            "code_verifier" in dict_values
            and "code_challenge" not in dict_values
            and "code_challenge_method" not in dict_values
        ):
            return dict_values
        elif (
            "code_verifier" not in dict_values
            and "code_challenge" in dict_values
            and "code_challenge_method" in dict_values
        ):
            return dict_values
        raise ValueError(
            "You can provide either code_verifier or "
            "code_challenge and code_challenge_method"
        )

    def is_to_check(self) -> bool:
        return bool(self.code_verifier)
