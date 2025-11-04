FROM python:3.14-slim AS build_stage

WORKDIR /app/

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Stage 2 -- Production Stage
FROM python:3.14-slim

WORKDIR /app/

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user
RUN useradd -m -r appuser && \
    chown -R appuser /app

# Copy Python dependencies from build stage
COPY --from=build_stage /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
COPY --from=build_stage /usr/local/bin/ /usr/local/bin/

# Copy the app
COPY --chown=appuser:appuser . .

# Switch user
USER appuser

# Documentation
EXPOSE 8081

RUN chmod +x /app/entrypoint.sh

CMD [ "/app/entrypoint.sh" ]