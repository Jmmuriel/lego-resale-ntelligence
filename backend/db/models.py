from datetime import date, datetime, timezone
from typing import Literal

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.database import Base


Condition = Literal["SEALED", "USED_COMPLETE", "USED_INCOMPLETE", "UNKNOWN"]


class SetCatalog(Base):
    """Expanded retired LEGO set catalog for V2."""

    __tablename__ = "set_catalog"

    set_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    theme: Mapped[str] = mapped_column(String(120), nullable=False)
    year_released: Mapped[int | None] = mapped_column(Integer)
    year_retired: Mapped[int | None] = mapped_column(Integer)
    retail_price_eur: Mapped[float | None] = mapped_column(Float)
    pieces: Mapped[int | None] = mapped_column(Integer)
    popularity_score: Mapped[int | None] = mapped_column(Integer)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    price_history: Mapped[list["PriceHistory"]] = relationship(back_populates="set_item")
    portfolio_items: Mapped[list["PortfolioItem"]] = relationship(back_populates="set_item")


class PriceHistory(Base):
    """Time-series price observations used by the dynamic pricing engine."""

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    set_id: Mapped[str] = mapped_column(ForeignKey("set_catalog.set_id"), index=True, nullable=False)
    condition: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    source: Mapped[str] = mapped_column(String(80), nullable=False)
    price_min_eur: Mapped[float] = mapped_column(Float, nullable=False)
    price_avg_eur: Mapped[float] = mapped_column(Float, nullable=False)
    price_max_eur: Mapped[float] = mapped_column(Float, nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    recorded_at: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    set_item: Mapped[SetCatalog] = relationship(back_populates="price_history")


class Listing(Base):
    """Analyzed marketplace listing with V2 market context."""

    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(30), default="analyzed", nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    marketplace: Mapped[str | None] = mapped_column(String(50))
    set_id: Mapped[str | None] = mapped_column(String(20), index=True)
    condition: Mapped[str | None] = mapped_column(String(30))
    asking_price_eur: Mapped[float | None] = mapped_column(Float)
    shipping_eur: Mapped[float | None] = mapped_column(Float)
    fair_price_eur: Mapped[float | None] = mapped_column(Float)
    fair_price_source: Mapped[str | None] = mapped_column(String(40))
    anomaly_score: Mapped[float | None] = mapped_column(Float)
    gross_margin_eur: Mapped[float | None] = mapped_column(Float)
    net_margin_eur: Mapped[float | None] = mapped_column(Float)
    opportunity_score: Mapped[int | None] = mapped_column(Integer)
    category: Mapped[str | None] = mapped_column(String(20))
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)


class PortfolioItem(Base):
    """Single-user holding in the LEGO resale portfolio."""

    __tablename__ = "portfolio_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    set_id: Mapped[str] = mapped_column(ForeignKey("set_catalog.set_id"), index=True, nullable=False)
    set_name: Mapped[str] = mapped_column(String(255), nullable=False)
    condition: Mapped[str] = mapped_column(String(30), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    cost_basis_eur: Mapped[float] = mapped_column(Float, nullable=False)
    purchased_at: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="HOLDING", nullable=False)
    sell_target_eur: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)

    set_item: Mapped[SetCatalog] = relationship(back_populates="portfolio_items")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="portfolio_item")


class Transaction(Base):
    """Portfolio buy/sell event for realized P&L tracking."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    portfolio_item_id: Mapped[int] = mapped_column(
        ForeignKey("portfolio_items.id"),
        index=True,
        nullable=False,
    )
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    amount_eur: Mapped[float] = mapped_column(Float, nullable=False)
    fees_eur: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    shipping_eur: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    happened_at: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    portfolio_item: Mapped[PortfolioItem] = relationship(back_populates="transactions")


class MarketBriefingRecord(Base):
    """Persisted market briefing generated locally or by Claude Sonnet."""

    __tablename__ = "market_briefings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    briefing_text: Mapped[str] = mapped_column(Text, nullable=False)
    key_opportunities: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    market_trend: Mapped[str] = mapped_column(String(20), nullable=False)
    model_version: Mapped[str] = mapped_column(String(80), nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    used_llm: Mapped[bool] = mapped_column(default=False, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
