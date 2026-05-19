import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


V2_DATABASE_URL = os.getenv("V2_DATABASE_URL") or os.getenv("DATABASE_URL") or "sqlite:///db/lri_v2.db"


class Base(DeclarativeBase):
    """Declarative base for V2 persistent models."""


def get_engine(database_url: str = V2_DATABASE_URL) -> Engine:
    """Create a SQLAlchemy engine that works for SQLite locally and Postgres in deploy."""
    _ensure_sqlite_parent_dir(database_url)
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

    return create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)


def get_session_factory(database_url: str = V2_DATABASE_URL) -> sessionmaker[Session]:
    """Return a session factory for V2 database operations."""
    return sessionmaker(bind=get_engine(database_url), expire_on_commit=False)


def init_v2_db(database_url: str = V2_DATABASE_URL) -> Engine:
    """Create all V2 tables for local demo use.

    Production deployments should use Alembic migrations instead.
    """
    from backend.db import models  # noqa: F401

    engine = get_engine(database_url)
    Base.metadata.create_all(engine)

    return engine


def _ensure_sqlite_parent_dir(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return

    raw_path = database_url.replace("sqlite:///", "", 1)
    if not raw_path or raw_path == ":memory:":
        return

    Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
