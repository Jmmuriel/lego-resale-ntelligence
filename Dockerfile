FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run as an unprivileged user. It owns /app so the boot script can still create
# the local SQLite file under db/ when no Postgres URL is configured.
RUN useradd --create-home --uid 10001 app && chown app:app /app
COPY --chown=app:app . .
USER app

CMD ["sh", "scripts/v2_boot_api.sh"]
