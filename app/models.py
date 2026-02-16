from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    func,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    )


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id"), nullable=True
    )
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    posts_count: Mapped[int] = mapped_column(BigInteger, default=0)
    posts_read_count: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_email: Mapped[str] = mapped_column(String(50), nullable=True)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", lazy="raise_on_sql"
    )
    profession: Mapped["Profession"] = relationship(
        back_populates="users", lazy="raise_on_sql"
    )

    def __repr__(self):
        return f"User({self.first_name} {self.last_name})"


class Post(BaseModel):
    __tablename__ = "post"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    body: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    mins_read: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="posts")
    category: Mapped["Category"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(
        secondary="post_tag",
        back_populates="posts",
        lazy="raise_on_sql",
    )

    def __repr__(self):
        return f"Post({self.title})"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="category", lazy="raise_on_sql"
    )

    def __repr__(self):
        return f"Category({self.name})"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    posts: Mapped[list["Post"]] = relationship(
        secondary="post_tag", back_populates="tags", lazy="raise_on_sql"
    )

    def __repr__(self):
        return f"Tag({self.name})"


class Profession(Base):
    __tablename__ = "professions"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))

    users: Mapped[list["User"]] = relationship(
        back_populates="profession", lazy="raise_on_sql"
    )

    def __repr__(self):
        return f"Profession({self.name})"


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    url: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f"Media({self.url})"


class PostMedia(Base):
    __tablename__ = "post_media"

    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"), primary_key=True
    )
    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id"), primary_key=True
    )


class Comment(BaseModel):
    __tablename__ = "comments"

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    text: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"Comment({self.id})"


class UserSearch(Base):
    __tablename__ = "user_searches"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    term: Mapped[str] = mapped_column(String(50), nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"UserSearch({self.term})"


class Device(BaseModel):
    __tablename__ = "devices"

    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    last_active: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self):
        return f"Device({self.user_agent})"


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id")
    )
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    def __repr__(self):
        return f"Like({self.id})"


post_tag_m2m_table = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", BigInteger, ForeignKey("post.id"), primary_key=True),
    Column("tag_id", BigInteger, ForeignKey("tags.id"), primary_key=True),
)
