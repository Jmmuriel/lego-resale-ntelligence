import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from src.models import ListingExtraction


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
MAX_TOKENS = 800


def extract_listing(raw_text: str) -> ListingExtraction:
    """Extrae datos estructurados de un listing usando Anthropic."""
    prompt = build_extraction_prompt(raw_text)
    response_text = call_anthropic(prompt)

    return parse_extraction_response(response_text)


def build_extraction_prompt(raw_text: str) -> str:
    """Construye el prompt de extracción a partir del texto crudo."""
    clean_text = _clean_raw_text(raw_text)
    if not clean_text:
        raise ValueError("El texto crudo del listing no puede estar vacío.")

    return f"""
Eres un extractor de datos para listings de LEGO descatalogado.
Devuelve exclusivamente un JSON válido, sin markdown y sin texto adicional.

Schema obligatorio:
{{
  "set_id": "str | null",
  "title_clean": "str",
  "condition": "SEALED | USED_COMPLETE | USED_INCOMPLETE | UNKNOWN",
  "description_summary": "str",
  "risk_flags": ["str"]
}}

Reglas:
- set_id debe ser un identificador LEGO de 4 a 6 dígitos si aparece claramente.
- Si no puedes identificar el set_id, usa null.
- title_clean debe ser un título limpio y breve.
- condition debe ser:
  - SEALED si el listing indica nuevo, precintado o sealed.
  - USED_COMPLETE si indica usado completo.
  - USED_INCOMPLETE si indica piezas faltantes, incompleto o sin minifiguras relevantes.
  - UNKNOWN si no queda claro.
- description_summary debe resumir el listing en máximo 200 caracteres.
- risk_flags debe contener riesgos concretos, por ejemplo:
  "Sin caja", "Sin instrucciones", "Piezas faltantes", "Faltan minifiguras",
  "Estado no claro", "Precio no verificable".
- Si no hay riesgos claros, devuelve una lista vacía.

Texto del listing:
{clean_text}
""".strip()


def call_anthropic(prompt: str) -> str:
    """Llama a Anthropic y devuelve el texto bruto de respuesta."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Falta ANTHROPIC_API_KEY en el entorno.")

    from anthropic import Anthropic, APIConnectionError, APIError, AuthenticationError

    client = Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
    except AuthenticationError as exc:
        raise RuntimeError(
            "La API key de Anthropic no es válida. Revisa ANTHROPIC_API_KEY en .env."
        ) from exc
    except APIConnectionError as exc:
        raise RuntimeError("No se pudo conectar con Anthropic.") from exc
    except APIError as exc:
        raise RuntimeError(f"Anthropic devolvió un error de API: {exc}") from exc

    return _anthropic_message_to_text(message)


def parse_extraction_response(response_text: str) -> ListingExtraction:
    """Valida la respuesta JSON del LLM contra ListingExtraction."""
    if not response_text or not response_text.strip():
        raise ValueError("La respuesta de extracción está vacía.")

    clean_response = _strip_markdown_json_block(response_text)

    try:
        data = json.loads(clean_response)
    except json.JSONDecodeError as exc:
        raise ValueError("La respuesta de extracción no es JSON válido.") from exc

    try:
        return ListingExtraction.model_validate(data)
    except ValidationError as exc:
        raise ValueError("La respuesta de extracción no cumple el schema esperado.") from exc


def _clean_raw_text(raw_text: str) -> str:
    """Normaliza espacios para reducir ruido antes de enviar al LLM."""
    return " ".join((raw_text or "").split())


def _strip_markdown_json_block(response_text: str) -> str:
    """Acepta respuestas envueltas en ```json sin cambiar el contrato JSON final."""
    text = response_text.strip()
    if not text.startswith("```"):
        return text

    lines = text.splitlines()
    if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()

    return text


def _anthropic_message_to_text(message) -> str:
    """Extrae texto de una respuesta de Anthropic."""
    text_blocks: list[str] = []

    for block in message.content:
        text = getattr(block, "text", None)
        if text:
            text_blocks.append(text)

    return "\n".join(text_blocks).strip()
