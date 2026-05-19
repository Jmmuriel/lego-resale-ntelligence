"""initial V2 schema

Revision ID: 20260517_0001
Revises:
Create Date: 2026-05-17
"""

from alembic import op
import sqlalchemy as sa


revision = "20260517_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "set_catalog",
        sa.Column("set_id", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("theme", sa.String(length=120), nullable=False),
        sa.Column("year_released", sa.Integer(), nullable=True),
        sa.Column("year_retired", sa.Integer(), nullable=True),
        sa.Column("retail_price_eur", sa.Float(), nullable=True),
        sa.Column("pieces", sa.Integer(), nullable=True),
        sa.Column("popularity_score", sa.Integer(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("set_id"),
    )
    op.create_table(
        "listings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("marketplace", sa.String(length=50), nullable=True),
        sa.Column("set_id", sa.String(length=20), nullable=True),
        sa.Column("condition", sa.String(length=30), nullable=True),
        sa.Column("asking_price_eur", sa.Float(), nullable=True),
        sa.Column("shipping_eur", sa.Float(), nullable=True),
        sa.Column("fair_price_eur", sa.Float(), nullable=True),
        sa.Column("fair_price_source", sa.String(length=40), nullable=True),
        sa.Column("anomaly_score", sa.Float(), nullable=True),
        sa.Column("gross_margin_eur", sa.Float(), nullable=True),
        sa.Column("net_margin_eur", sa.Float(), nullable=True),
        sa.Column("opportunity_score", sa.Integer(), nullable=True),
        sa.Column("category", sa.String(length=20), nullable=True),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_listings_set_id"), "listings", ["set_id"], unique=False)
    op.create_table(
        "market_briefings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("briefing_text", sa.Text(), nullable=False),
        sa.Column("key_opportunities", sa.JSON(), nullable=False),
        sa.Column("market_trend", sa.String(length=20), nullable=False),
        sa.Column("model_version", sa.String(length=80), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("used_llm", sa.Boolean(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "portfolio_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("set_id", sa.String(length=20), nullable=False),
        sa.Column("set_name", sa.String(length=255), nullable=False),
        sa.Column("condition", sa.String(length=30), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("cost_basis_eur", sa.Float(), nullable=False),
        sa.Column("purchased_at", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("sell_target_eur", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["set_id"], ["set_catalog.set_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_portfolio_items_set_id"), "portfolio_items", ["set_id"], unique=False)
    op.create_table(
        "price_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("set_id", sa.String(length=20), nullable=False),
        sa.Column("condition", sa.String(length=30), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("price_min_eur", sa.Float(), nullable=False),
        sa.Column("price_avg_eur", sa.Float(), nullable=False),
        sa.Column("price_max_eur", sa.Float(), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("recorded_at", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["set_id"], ["set_catalog.set_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_price_history_condition"), "price_history", ["condition"], unique=False)
    op.create_index(op.f("ix_price_history_recorded_at"), "price_history", ["recorded_at"], unique=False)
    op.create_index(op.f("ix_price_history_set_id"), "price_history", ["set_id"], unique=False)
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("portfolio_item_id", sa.Integer(), nullable=False),
        sa.Column("transaction_type", sa.String(length=20), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("amount_eur", sa.Float(), nullable=False),
        sa.Column("fees_eur", sa.Float(), nullable=False),
        sa.Column("shipping_eur", sa.Float(), nullable=False),
        sa.Column("happened_at", sa.Date(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["portfolio_item_id"], ["portfolio_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_transactions_portfolio_item_id"),
        "transactions",
        ["portfolio_item_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_transactions_portfolio_item_id"), table_name="transactions")
    op.drop_table("transactions")
    op.drop_index(op.f("ix_price_history_set_id"), table_name="price_history")
    op.drop_index(op.f("ix_price_history_recorded_at"), table_name="price_history")
    op.drop_index(op.f("ix_price_history_condition"), table_name="price_history")
    op.drop_table("price_history")
    op.drop_index(op.f("ix_portfolio_items_set_id"), table_name="portfolio_items")
    op.drop_table("portfolio_items")
    op.drop_table("market_briefings")
    op.drop_index(op.f("ix_listings_set_id"), table_name="listings")
    op.drop_table("listings")
    op.drop_table("set_catalog")
