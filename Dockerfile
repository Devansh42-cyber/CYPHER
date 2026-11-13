# ---- CYPHER: AI Phishing URL Detection (Flask) ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=5000 \
    APP_ENV=production \
    APP_VERSION=dev

WORKDIR /app

# Install dependencies first so this layer is cached between code changes
COPY cypher/requirements.txt .
RUN pip install -r requirements.txt

# Copy the application (anything listed in .dockerignore is skipped)
COPY cypher/ .

# "Build" step: byte-compile sources and fail early if the model can't be loaded
RUN python -m compileall -q . \
 && python -c "import joblib; joblib.load('model/phishing_model.pkl')"

# Run as an unprivileged user
RUN useradd --create-home --uid 10001 appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:%s/health' % os.environ.get('PORT','5000'), timeout=4)" || exit 1

# One worker keeps the in-memory dashboard stats consistent; threads handle concurrency
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 4 --access-logfile - app:app"]
