from pydantic import BaseModel, field_validator, ValidationError


class RefreshTokenPayload(BaseModel):
    type: str = "refresh"
    user_id: str

    @field_validator("type")
    @classmethod
    def type_must_equal_refresh(cls, type: str) -> str:
        if type != "refresh":
            raise ValidationError("type must equal refresh")
        return type
