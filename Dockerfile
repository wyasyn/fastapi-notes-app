FROM python:3.12-slim

# Create non‑root user
RUN useradd -m appuser

WORKDIR /app

# Copy & install dependencies (make sure python-multipart is in requirements.txt!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Fix ownership, drop back to non‑root
RUN chown -R appuser:appuser /app
USER appuser

# Let Render know which port you'll listen on
# (optional but self‑documenting)
ARG PORT=8080
ENV PORT=${PORT}

# Tell Docker which port you listen on
EXPOSE ${PORT}

# Use the PORT env var (fallback 8080) in your startup cmd
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
