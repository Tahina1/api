from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI(title="Snip API - v0")

class LinkCreate(BaseModel): # input DTO
    target_url: HttpUrl
    slug: str = Field(pattern=r"^[A-Za-z0-9_-]{3,32}$")
    title: str | None = Field(default=None, max_length=200)

class LinkOut(BaseModel): # output
    slug: str
    target_url: str
    title: str | None
    created_at: datetime

_links: dict[str, LinkOut] = {} # database

class Pagination(BaseModel):
    limit: int
    offset: int

def pagination(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Pagination:
    return Pagination(limit=limit, offset=offset)

PageDep = Annotated[Pagination, Depends(pagination)]

@app.post("/links", status_code=status.HTTP_201_CREATED)
async def create_link(data: LinkCreate) -> LinkOut: # JSON body
    if data.slug in _links:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="slug taken")
    link = LinkOut(
        slug=data.slug,
        target_url=str(data.target_url),
        title=data.title,
        created_at=datetime.now(UTC)
    )
    _links[data.slug] = link
    return link


@app.get("/links")
async def list_links(page: PageDep, q: str | None = None) -> list[LinkOut]:
    items = list(_links.values())
    if q:
        items = [link for link in items if q.lower() in (link.title or "").lower()]
    return items[page.offset: page.offset + page.limit]

@app.get("/links/{slug}")
async def get_linl(slug: str) -> LinkOut:
    link = _links.get(slug)
    if link is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Link Not Found")
    return link