#!/usr/bin/env bash

set -e

if ! command -v python3 >/dev/null 2>&1; then
  echo "No se encontró python3."
  echo "Instala Python 3 antes de ejecutar el setup."
  exit 1
fi

echo "Creando entorno virtual con Python 3..."
python3 -m venv .venv

echo "Instalando dependencias..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo ""
echo "Setup completado."
echo "Siguiente paso:"
echo "  source .venv/bin/activate"
echo "  streamlit run app/main.py"
echo ""
echo "Para V2:"
echo "  cd frontend && npm install"
echo "  .venv/bin/alembic upgrade head"
echo "  .venv/bin/python scripts/v2_validate_seed_data.py"
echo "  .venv/bin/python scripts/v2_check_candidate_readiness.py"
echo "  .venv/bin/python scripts/v2_seed_db.py"
echo "  bash scripts/v2_start_api.sh"
echo "  bash scripts/v2_start_frontend.sh"
echo ""
echo "Para ejecutar tests:"
echo "  pytest"
