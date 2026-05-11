from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ListingInput(BaseModel):
    """Datos de entrada capturados desde un listing antes del análisis."""

    model_config = ConfigDict(str_strip_whitespace=True)

    url: str | None = None
    marketplace: str | None = None
    raw_title: str | None = None
    raw_description: str | None = None
    asking_price_eur: float | None = Field(default=None, ge=0)
    shipping_eur: float | None = Field(default=None, ge=0)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str | None) -> str | None:
        if value is not None and not value:
            raise ValueError("La URL no puede estar vacía.")
        return value


class ListingExtraction(BaseModel):
    """Información limpia extraída de un listing."""

    model_config = ConfigDict(str_strip_whitespace=True)

    set_id: str | None = None
    title_clean: str
    condition: Literal["SEALED", "USED_COMPLETE", "USED_INCOMPLETE", "UNKNOWN"]
    description_summary: str
    risk_flags: list[str] = Field(default_factory=list)

    @field_validator("title_clean", "condition", "description_summary")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value:
            raise ValueError("Este campo no puede estar vacío.")
        return value


class CatalogSet(BaseModel):
    """Set LEGO retirado disponible en el catálogo local."""

    model_config = ConfigDict(str_strip_whitespace=True)

    set_id: str
    name: str
    theme: str
    year_released: int
    year_retired: int
    retail_price_eur: float = Field(ge=0)
    pieces: int = Field(ge=0)
    popularity_score: int = Field(ge=1, le=10)

    @field_validator("set_id", "name", "theme")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value:
            raise ValueError("Este campo no puede estar vacío.")
        return value


class ListingAnalysis(BaseModel):
    """Resultado final del análisis de oportunidad de compra."""

    model_config = ConfigDict(str_strip_whitespace=True)

    url: str
    marketplace: str | None = None
    set_id: str | None = None
    condition: Literal["SEALED", "USED_COMPLETE", "USED_INCOMPLETE", "UNKNOWN"] | None = None
    asking_price_eur: float | None = Field(default=None, ge=0)
    shipping_eur: float | None = Field(default=None, ge=0)
    fair_price_eur: float | None = Field(default=None, ge=0)
    gross_margin_eur: float | None = None
    net_margin_eur: float | None = None
    opportunity_score: int | None = Field(default=None, ge=0, le=100)
    category: Literal["GREEN", "YELLOW", "RED"] | None = None
    risk_flags: list[str] = Field(default_factory=list)
    notes: str | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not value:
            raise ValueError("La URL no puede estar vacía.")
        return value
