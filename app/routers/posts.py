from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Post, post_tag_m2m_table, Tag
from app.database import db_dep
from app.schemas.schemas import PostListResponse, PostCreateRequest, PostUpdateRequest
from app.utils import generate_slug


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostListResponse])
async def get_posts(
    session: db_dep,
    is_active: bool | None = None,
    category_id: int | None = None,
    tag_id: int | None = None,
):
    stmt = (
        select(Post)
        .join(post_tag_m2m_table, Post.id == post_tag_m2m_table.c.post_id)
        .join(Tag, post_tag_m2m_table.c.tag_id == Tag.id)
    )

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    if category_id:
        stmt = stmt.where(Post.category_id == category_id)

    if tag_id:
        stmt = stmt.where(Tag.id == tag_id)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()


@router.get("/{slug}/", response_model=PostListResponse)
async def get_post(session: db_dep, slug: str):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/post/create/")
async def post_create(session: db_dep, create_data: PostCreateRequest):
    post = Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@router.put("/posts/")
async def post_update(session: db_dep, post_id: int, update_data: PostUpdateRequest):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.title:
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body:
        post.body = update_data.body

    if update_data.is_active:
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)

    return post


@router.patch("/posts/")
async def post_update_patch(
    session: db_dep, post_id: int, update_data: PostUpdateRequest
):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.title:
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body:
        post.body = update_data.body

    if update_data.is_active:
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)

    return post


@router.delete("/posts/", status_code=204)
async def post_delete(session: db_dep, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()