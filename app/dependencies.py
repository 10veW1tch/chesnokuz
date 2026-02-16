from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import db_dep
from app.models import User
from app.utils import verify_password


basic = HTTPBasic()
basic_auth_dep = Annotated[HTTPBasicCredentials, Depends(basic)]


def get_current_user(session: db_dep, credentials: basic_auth_dep):
    stmt = (
        select(User)
        .where(User.email == credentials.username)
        .options(joinedload(User.profession))
    )
    user = session.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


current_user_basic_dep = Annotated[User, Depends(get_current_user)]