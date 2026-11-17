FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY config.py run.py ./

RUN mkdir -p /app/instance && chown -R app:app /app
USER app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:5000/health', timeout=3).read()"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--preload", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
