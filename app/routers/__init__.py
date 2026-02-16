from .posts import router as posts_router
from .tag import router as tags_router
from .category import router as category_router
from .profession import router as profession_router
from .weather import router as weather_router
from .users import router as users_router
from .lesson import router as lesson_router
from .auth import auth_router


__all__ = [
    "posts_router",
    "tags_router",
    "category_router",
    "profession_router",
    "weather_router",
    "users_router",
    "lesson_router",
    "auth_router"
]