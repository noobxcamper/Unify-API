FROM python:3.12-slim AS build_stage

WORKDIR /app/

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --break-system-packages -r /app/requirements.txt


# --------------------------------------------
# Stage 2 -- Production Stage
# --------------------------------------------
FROM python:3.12-slim

WORKDIR /app/

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install runtime dependency needed by mysqlclient
RUN apt-get update && apt-get install -y \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -r appuser && \
    chown -R appuser /app

# Copy Python dependencies from build stage
COPY --from=build_stage /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=build_stage /usr/local/bin/ /usr/local/bin/

# Copy the app code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8081

RUN chmod +x /app/entrypoint.sh

CMD [ "/app/entrypoint.sh" ]