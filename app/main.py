from fastapi import FastAPI

from app.routers import (
    auth_router,
    posts_router,
    tags_router,
    category_router,
    profession_router,
    weather_router,
    users_router,
    lesson_router,
)


app = FastAPI(
    title="Chesnokdek yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(category_router)
app.include_router(profession_router)
app.include_router(weather_router)
app.include_router(users_router)
app.include_router(lesson_router)