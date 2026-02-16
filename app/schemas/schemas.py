from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostCreateRequest(BaseModel):
    title: str
    body: str


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    is_active: bool
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 6,
                    "title": "O'zbekistonning YaIM si 130 mlrddan oshdi.",
                    "slug": "ozbekistonning-yaim-si-130-mlrddan-oshdi",
                    "body": "O'zbekiston Markaziy Osiyodagi eng kuchli davlat boldi",
                    "is_active": True,
                    "created_at": "2026-19-01T13:01:18.001Z",
                }
            ]
        }
    }


class PostUpdateRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    is_active: bool | None = None


class TagCreateRequest(BaseModel):
    name: str
    slug: str


class TagUpdateRequest(BaseModel):
    name: str | None = None


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str


class CategoryListResonse(BaseModel):
    id: int | None = None
    name: str | None = None


class CategoryCreateRequest(BaseModel):
    name: str | None = None


class ProfessionCreateRequest(BaseModel):
    name: str


class ProfessionListResponse(BaseModel):
    id: int
    name: str


class ProfessionUpdateRequest(BaseModel):
    name: str


class WeatherCoord(BaseModel):
    lon: float
    lat: float


class WeatherInline(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class WeatherMainInline(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class WeatherResponse(BaseModel):
    coord: WeatherCoord
    weather: list[WeatherInline]
    # base: str
    # main: WeatherMainInline
    # visibility: int
    # wind: dict[str, float] | None = None
    # rain: dict[str, float] | None = None
    # clouds: dict[str, int] | None = None
    # dt: int
    # sys: dict[str, int | str] | None = None
    # timezone: int
    # id: int
    # name: str
    # cod: int


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None