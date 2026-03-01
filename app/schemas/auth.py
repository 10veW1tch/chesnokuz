from pydantic import AliasChoices, BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_staff: bool
    is_superuser: bool
    is_active: bool

    model_config = {
        "from_attributes": True,
    }


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    profession_id: int | None = None
    bio: str | None = None
    is_active: bool
    is_staff: bool
    is_superuser: bool

    model_config = {
        "from_attributes": True,
    }


class UserProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    profession_id: int | None = None
    bio: str | None = None


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(validation_alias=AliasChoices("email", "username"))
    password: str

    model_config = {
        "extra": "ignore",
    }


class RefreshTokenRequest(BaseModel):
    refresh_token: str
