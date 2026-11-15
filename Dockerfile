# MediCheck AI server (CPU only). Build from the repo root: docker compose up --build
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencies first so code changes do not reinstall them
COPY backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

# Server code + final models (out/onnx_final, without detector.pt: see .dockerignore)
COPY backend backend
COPY out/onnx_final out/onnx_final

RUN useradd --create-home --uid 10001 app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health', timeout=4)" || exit 1

CMD ["python", "-m", "uvicorn", "backend.medicheck_server.app:app", "--host", "0.0.0.0", "--port", "8000"]
