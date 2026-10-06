import secrets
import string

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Link
from app.schemas import LinkCreate, LinkOut, LinkUpdate, TopLink

CLICKS_KEY = "links:clicks" # sorted set : membre = slug, score = nombre de clics
ALPHABET = string.ascii_letters + string.digits

# ---------- Exceptions métier (traduites en HTTP dans main.py) ----------
class LinkNotFound(Exception):
    pass

class SlugAlreadyTaken(Exception):
    pass

# ---------- Helpers ----------
def cache_key(slug: str) -> str:
    return f"link:{slug}"

def generate_slug(length: int = 7) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

def to_out(link: Link, clicks: int = 0) -> LinkOut:
    return LinkOut.model_validate(link).model_copy(update={"clicks": clicks})
