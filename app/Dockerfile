# Stage 1: Builder
FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY ./ecommerce-app/requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./ecommerce-app/ .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["python3", "application.py"]