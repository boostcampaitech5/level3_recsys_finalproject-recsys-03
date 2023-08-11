from pydantic import BaseModel, field_validator, ValidationError


class AccessTokenPayload(BaseModel):
    type: str = "access"
    user_id: str

    @field_validator("type")
    @classmethod
    def type_must_equal_access(cls, type: str) -> str:
        if type != "access":
            raise ValidationError("type must equal access")
        return type
