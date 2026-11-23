FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir selenium==4.35.0 pytest==8.4.1
WORKDIR /workspace
