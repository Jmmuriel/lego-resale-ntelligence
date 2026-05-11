import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import DateTime, Float, Integer, JSON, String, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from src.models import ListingAnalysis


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db/lri.db")
VALID_STATUSES = {"analyzed", "watching", "discarded", "bought"}


class Base(DeclarativeBase):
    """Base declarativa de SQLAlchemy para las tablas locales."""


class ListingAnalysisRecord(Base):
    """Registro persistente de un listing analizado."""

    __tablename__ = "listing_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(30), default="analyzed", nullable=False)

    url: Mapped[str] = mapped_column(String, nullable=False)
    marketplace: Mapped[str | None] = mapped_column(String(50))
    set_id: Mapped[str | None] = mapped_column(String(20))
    condition: Mapped[str | None] = mapped_column(String(30))
    asking_price_eur: Mapped[float | None] = mapped_column(Float)
    shipping_eur: Mapped[float | None] = mapped_column(Float)
    fair_price_eur: Mapped[float | None] = mapped_column(Float)
    gross_margin_eur: Mapped[float | None] = mapped_column(Float)
    net_margin_eur: Mapped[float | None] = mapped_column(Float)
    opportunity_score: Mapped[int | None] = mapped_column(Integer)
    category: Mapped[str | None] = mapped_column(String(20))
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    notes: Mapped[str | None] = mapped_column(String)


def init_db(database_url: str = DATABASE_URL) -> Engine:
    """Inicializa la base SQLite local y crea las tablas si no existen."""
    _ensure_sqlite_parent_dir(database_url)
    engine = _create_engine(database_url)
    Base.metadata.create_all(engine)

    return engine


def save_listing_analysis(
    analysis: ListingAnalysis,
    database_url: str = DATABASE_URL,
    status: str = "analyzed",
) -> ListingAnalysisRecord:
    """Guarda un análisis de listing en SQLite."""
    _validate_status(status)
    session_factory = _session_factory(database_url)

    with session_factory() as session:
        record = ListingAnalysisRecord(
            status=status,
            url=analysis.url,
            marketplace=analysis.marketplace,
            set_id=analysis.set_id,
            condition=analysis.condition,
            asking_price_eur=analysis.asking_price_eur,
            shipping_eur=analysis.shipping_eur,
            fair_price_eur=analysis.fair_price_eur,
            gross_margin_eur=analysis.gross_margin_eur,
            net_margin_eur=analysis.net_margin_eur,
            opportunity_score=analysis.opportunity_score,
            category=analysis.category,
            risk_flags=analysis.risk_flags,
            notes=analysis.notes,
        )
        session.add(record)
        session.commit()
        session.refresh(record)

        return record


def list_recent_listings(
    limit: int = 20,
    database_url: str = DATABASE_URL,
) -> list[ListingAnalysisRecord]:
    """Lista los últimos análisis guardados."""
    session_factory = _session_factory(database_url)

    with session_factory() as session:
        statement = (
            select(ListingAnalysisRecord)
            .order_by(ListingAnalysisRecord.created_at.desc(), ListingAnalysisRecord.id.desc())
            .limit(limit)
        )
        return list(session.scalars(statement).all())


def update_listing_status(
    listing_id: int,
    status: str,
    database_url: str = DATABASE_URL,
) -> ListingAnalysisRecord | None:
    """Actualiza el estado manual de un listing guardado."""
    _validate_status(status)
    session_factory = _session_factory(database_url)

    with session_factory() as session:
        record = session.get(ListingAnalysisRecord, listing_id)
        if record is None:
            return None

        record.status = status
        session.commit()
        session.refresh(record)

        return record


def _session_factory(database_url: str) -> sessionmaker[Session]:
    engine = init_db(database_url)
    return sessionmaker(bind=engine, expire_on_commit=False)


def _create_engine(database_url: str) -> Engine:
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    return create_engine(database_url, connect_args=connect_args)


def _ensure_sqlite_parent_dir(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return

    raw_path = database_url.replace("sqlite:///", "", 1)
    if not raw_path or raw_path == ":memory:":
        return

    Path(raw_path).parent.mkdir(parents=True, exist_ok=True)


def _validate_status(status: str) -> None:
    if status not in VALID_STATUSES:
        valid_values = ", ".join(sorted(VALID_STATUSES))
        raise ValueError(f"Estado inválido: {status}. Valores válidos: {valid_values}.")
